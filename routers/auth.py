from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from business.auth_logic import AuthLogic
from dbcon import get_db
from models.user_model import UserRole, User

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="frontend")

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    user_role = request.session.get("role")
    if user_role == UserRole.participant.value:
        return RedirectResponse(url="/participants/dashboard", status_code=302)
    elif user_role == UserRole.questioner.value:
        return RedirectResponse(url="/questioners/dashboard", status_code=302)
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_role = request.session.get("role")
    if user_role == UserRole.participant.value:
        return RedirectResponse(url="/participants/dashboard", status_code=302)
    elif user_role == UserRole.questioner.value:
        return RedirectResponse(url="/questioners/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        user_id = await AuthLogic.signup(username, email, password, role, db)
        request.session["user_id"] = user_id
        request.session["role"] = role
        if role == UserRole.participant.value:
            return RedirectResponse(url="/participants/dashboard", status_code=302)
        elif role == UserRole.questioner.value:
            return RedirectResponse(url="/questioners/dashboard", status_code=302)
    except HTTPException as e:
        return {"message": e.detail}, e.status_code

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        user_id = await AuthLogic.login(email, password, db)
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one()
        request.session["user_id"] = user_id
        request.session["role"] = user.role.value
        if user.role == UserRole.participant:
            return RedirectResponse(url="/participants/dashboard", status_code=302)
        elif user.role == UserRole.questioner:
            return RedirectResponse(url="/questioners/dashboard", status_code=302)
    except HTTPException as e:
        return {"message": e.detail}, e.status_code

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/auth/login", status_code=302)
