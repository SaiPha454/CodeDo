from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.user_model import UserRole

templates = Jinja2Templates(directory="frontend/main/questioner")

questioner_router = APIRouter(prefix="/questioners", tags=["questioners"])

def verify_role(request: Request, required_role: UserRole):
    user_role = request.session.get("role")
    if user_role != required_role.value:
        raise HTTPException(status_code=403, detail="Access forbidden")

@questioner_router.get("/dashboard", response_class=HTMLResponse)
async def questioner_dashboard(request: Request):
    verify_role(request, UserRole.questioner)
    return templates.TemplateResponse("dashboard.html", {"request": request})