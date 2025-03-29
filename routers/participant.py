from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.user_model import UserRole

templates = Jinja2Templates(directory="frontend/main/participant")

participant_router = APIRouter(prefix="/participants", tags=["participants"])

def verify_role(request: Request, required_role: UserRole):
    user_role = request.session.get("role")
    if user_role != required_role.value:
        raise HTTPException(status_code=403, detail="Access forbidden")

@participant_router.get("/dashboard", response_class=HTMLResponse)
async def participant_dashboard(request: Request):
    verify_role(request, UserRole.participant)
    return templates.TemplateResponse("dashboard.html", {"request": request})