from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from config.dbcon import get_db
from services.auth_service import AuthLogic
from repositories.challenge_model import Challenge
from repositories.user_model import User
from sqlalchemy.future import select

from middlewares.role_middleware import RoleMiddleware
from services.participant_challenge_service import ParticipantChallengeService
from repositories.user_model import UserRole
from routers.auth_router import AuthLogic
router = APIRouter(prefix="/participants/challenges", tags=["participants"])


# Initialize Jinja2Templates for rendering HTML templates
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_participant_challenges(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse("401.html", {"request": request}, status_code=401)

    # Verify the user's role
    RoleMiddleware.verify_role(request, UserRole.participant)

    # Fetch challenges for the participant
    challenges = await ParticipantChallengeService.get_participant_challenges(user_id, db)
    return templates.TemplateResponse("participant/dashboard.html", {"request": request, "challenges": challenges})

@router.get("/{challenge_id}", response_class=HTMLResponse)
async def get_challenge_problems(request: Request, challenge_id: int, db: AsyncSession = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse("401.html", {"request": request}, status_code=401)

    # Verify the user's role
    RoleMiddleware.verify_role(request, UserRole.participant)

    # Fetch the challenge details
    challenge = await ParticipantChallengeService.get_challenge_details(user_id, challenge_id, db)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    print(challenge)
    return templates.TemplateResponse("participant/challenge_problems.html", {"request": request, "challenge": challenge})