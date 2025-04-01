from fastapi import APIRouter, HTTPException, Depends, Request, Body
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from services.questioner_challenge_service import QuestionerChallengeService
from config.dbcon import get_db

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/questioners/challenges", tags=["challenges"])

@router.get("/")
async def display_challenges(request: Request, db: AsyncSession = Depends(get_db)):
    challenges = await QuestionerChallengeService.display_challenges(request, db)
    return templates.TemplateResponse(
        "questioner/dashboard.html", {"request": request, "challenges": challenges}
    )

@router.post("/")
async def create_challenge(
    request: Request,
    title: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    await QuestionerChallengeService.create_challenge(request, title, db)
    challenges = await QuestionerChallengeService.display_challenges(request, db)
    return templates.TemplateResponse(
        "questioner/dashboard.html", {"request": request, "challenges": challenges}
    )

@router.get("/{id}/")
async def get_challenge(id: int, db: AsyncSession = Depends(get_db)):
    return await QuestionerChallengeService.get_challenge(id, db)

@router.delete("/{id}/")
async def delete_challenge(id: int, request: Request, db: AsyncSession = Depends(get_db)):
    challenges = await QuestionerChallengeService.delete_challenge(request, id, db)
    return templates.TemplateResponse(
        "questioner/dashboard.html", {"request": request, "challenges": challenges}
    )