from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service import AuthLogic
from config.dbcon import get_db
from repositories.user_model import UserRole

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    user_role = request.session.get("role")
    if user_role:
        return await AuthLogic.redirect_based_on_role(user_role)
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_role = request.session.get("role")
    if user_role:
        return await AuthLogic.redirect_based_on_role(user_role)
    return templates.TemplateResponse("auth/login.html", {"request": request})

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
        await AuthLogic.setup_session(request, user_id, role)
        return await AuthLogic.redirect_based_on_role(role)
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
        user_id, role = await AuthLogic.login(email, password, db)
        await AuthLogic.setup_session(request, user_id, role)
        return await AuthLogic.redirect_based_on_role(role)
    except HTTPException as e:
        return {"message": e.detail}, e.status_code

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/auth/login", status_code=302)
