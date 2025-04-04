from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from repositories.user_model import UserRole
from config.dbcon import get_db
from middlewares.role_middleware import RoleMiddleware
from routers.questioner_challenge_router import display_challenges

# from routers.challenge import list_challenges
# from routers.problem import list_problems_for_challenge, show_problem_creation_form, show_problem_edit_form, show_problem_add_test_case_form



templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/questioners", tags=["questioners"])


@router.get("/dashboard", response_class=HTMLResponse)
async def display_questioner_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    return await display_challenges(request, db)

