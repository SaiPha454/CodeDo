from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import UserRole
from dbcon import get_db
from routers.challenge import list_challenges
from routers.problem import list_problems_for_challenge, show_problem_creation_form, show_problem_edit_form, show_problem_add_test_case_form

templates = Jinja2Templates(directory="frontend/main/questioner")

questioner_router = APIRouter(prefix="/questioners", tags=["questioners"])

def verify_role(request: Request, required_role: UserRole):
    user_role = request.session.get("role")
    if user_role != required_role.value:
        raise HTTPException(status_code=403, detail="Access forbidden")

@questioner_router.get("/dashboard", response_class=HTMLResponse)
async def display_questioner_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    verify_role(request, UserRole.questioner)
    return await list_challenges(request, db)


@questioner_router.get("/challenges/{challenge_id}/problems")
async def display_problems_dashboard_for_challenge(challenge_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    verify_role(request, UserRole.questioner)
    return await list_problems_for_challenge(challenge_id, request, db)


@questioner_router.get("/challenges/{challenge_id}/problems/new", response_class=HTMLResponse)
async def display_problem_creation_form(challenge_id: int, request: Request):
    verify_role(request, UserRole.questioner)
    return await show_problem_creation_form(challenge_id, request)

@questioner_router.get("/challenges/{challenge_id}/problems/{problem_id}/edit", response_class=HTMLResponse)
async def display_problem_edit_form(challenge_id: int, problem_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    verify_role(request, UserRole.questioner)
    return await show_problem_edit_form(challenge_id, problem_id, request, db)

@questioner_router.get("/problems/{problem_id}/testcases", response_class=HTMLResponse)
async def display_test_cases_for_problem(problem_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    verify_role(request, UserRole.questioner)
    return await show_problem_add_test_case_form(problem_id, request, db)

