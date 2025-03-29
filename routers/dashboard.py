from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from business.dashboard_logic import DashboardLogic

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = Jinja2Templates(directory="frontend")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not DashboardLogic.is_logged_in(request):
        return RedirectResponse(url="/auth/login", status_code=302)
    return templates.TemplateResponse("main/dashboard.html", {"request": request, "user_id": request.session["user_id"]})
