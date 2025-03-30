from fastapi import APIRouter, HTTPException, Depends, Request, Body
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.challenge import Challenge
from models.user_model import UserRole
from dbcon import get_db
from datetime import datetime

templates = Jinja2Templates(directory="frontend/main/questioner")

challenge_router = APIRouter(prefix="/challenges", tags=["challenges"])

def verify_questioner_role(request: Request):
    user_role = request.session.get("role")
    if user_role != UserRole.questioner.value:
        raise HTTPException(status_code=403, detail="Access forbidden")

@challenge_router.post("/")
async def create_challenge(
    request: Request,
    title: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    verify_questioner_role(request)
    user_id = request.session.get("user_id")
    new_challenge = Challenge(title=title, created_by=user_id)
    db.add(new_challenge)
    await db.commit()

    # Fetch updated challenges list
    result = await db.execute(select(Challenge).where(Challenge.created_by == user_id))
    challenges = result.scalars().all()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "challenges": challenges}
    )

@challenge_router.get("/")
async def list_challenges(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await db.execute(select(Challenge).where(Challenge.created_by == user_id))
    challenges = result.scalars().all()

    # Format the created_at field for human-readable display
    for challenge in challenges:
        challenge.created_at = challenge.created_at.strftime("%B %d, %Y %I:%M %p")

    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "challenges": challenges}
    )

@challenge_router.get("/{id}/")
async def get_challenge(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Challenge).where(Challenge.id == id))
    challenge = result.scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge