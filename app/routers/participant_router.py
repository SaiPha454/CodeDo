from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers import participant_challenge_router
from config.dbcon import get_db

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/participants", tags=["participants"])


@router.get("/dashboard", response_class=HTMLResponse)
async def get_participant_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    return await participant_challenge_router.get_participant_challenges(request, db)