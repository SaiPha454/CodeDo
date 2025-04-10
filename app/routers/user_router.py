from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from services.auth_service import AuthLogic
from fastapi.templating import Jinja2Templates
from config.dbcon import get_db
from fastapi import Depends, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService
from repositories.user_model import UserRole
from fastapi.responses import RedirectResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_user(request: Request, db: AsyncSession = Depends(get_db)):
    user = request.session.get("user_id")
    if not user:
        return templates.TemplateResponse("index.html", {"request": request})
    user = await AuthLogic.get_current_user(request=request, db=db)
    if user.role == UserRole.participant:
        return RedirectResponse(url="/participants/dashboard", status_code=302)
    elif user.role == UserRole.questioner:
        return RedirectResponse(url="/questioners/dashboard", status_code=302)

@router.get("/me/profile", response_class=HTMLResponse)
async def get_user_profile(request: Request, db: AsyncSession = Depends(get_db)):
    user = await AuthLogic.get_current_user(request=request, db=db)
    user.role = "Participant" if user.role == UserRole.participant else "Questioner"
    return templates.TemplateResponse(
        "user_profile.html", {"request": request, "user": user}
    )

@router.put("/me/profile")
async def update_user_name(request: Request, name: str = Body(...), db: AsyncSession = Depends(get_db)):
    return await UserService.update_user_name(request=request, new_username=name, db=db)
    