from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_challenge_participant(request: Request, challenge_id : int):
    
    return templates.TemplateResponse("questioner/challenge_participants.html", {"request": request})
