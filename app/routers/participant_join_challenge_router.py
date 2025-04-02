from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from config.dbcon import get_db
from services.auth_service import AuthLogic
from repositories.challenge_model import Challenge
from repositories.user_model import User
from sqlalchemy.future import select
from services.join_challenge_service import JoinChallengeService
from middlewares.role_middleware import RoleMiddleware

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/join-challenge")
async def join_challenge(request: Request, challenge_id: int = Query(..., description="ID of the challenge to join"), 
                         db: AsyncSession = Depends(get_db)):

    user = await JoinChallengeService.validate_user(request, db)
    challenge = await JoinChallengeService.get_challenge(request, challenge_id, db)
    print(challenge)
    return templates.TemplateResponse("participant/join_challenge.html", {"request": request, "challenge": challenge, "user": user})

@router.post("/join-challenge/{challenge_id}")
async def join_challenge(request: Request, challenge_id: int, db: AsyncSession = Depends(get_db)):
    current_user = await AuthLogic.get_current_user(request, db)
    join_challenge = await JoinChallengeService.join_challenge(request, current_user.id, challenge_id, db)
    return join_challenge