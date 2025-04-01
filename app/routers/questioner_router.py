from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from repositories.user_model import UserRole
from config.dbcon import get_db
from middlewares.role_middleware import RoleMiddleware


# from routers.challenge import list_challenges
# from routers.problem import list_problems_for_challenge, show_problem_creation_form, show_problem_edit_form, show_problem_add_test_case_form



templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/questioners", tags=["questioners"])


@router.get("/dashboard", response_class=HTMLResponse)
async def display_questioner_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    RoleMiddleware.verify_role(request, UserRole.questioner)
    # return await list_challenges(request, db)
    return "Welcome to the Questioner Dashboard!"


@router.get("/challenges/{challenge_id}/problems")
async def display_problems_dashboard_for_challenge(challenge_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    RoleMiddleware.verify_role(request, UserRole.questioner)
    return await list_problems_for_challenge(challenge_id, request, db)


@router.get("/challenges/{challenge_id}/problems/new", response_class=HTMLResponse)
async def display_problem_creation_form(challenge_id: int, request: Request):
    RoleMiddleware.verify_role(request, UserRole.questioner)
    return await show_problem_creation_form(challenge_id, request)

@router.get("/challenges/{challenge_id}/problems/{problem_id}/edit", response_class=HTMLResponse)
async def display_problem_edit_form(challenge_id: int, problem_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    RoleMiddleware.verify_role(request, UserRole.questioner)
    return await show_problem_edit_form(challenge_id, problem_id, request, db)

@router.get("/problems/{problem_id}/testcases", response_class=HTMLResponse)
async def display_test_cases_for_problem(problem_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    RoleMiddleware.verify_role(request, UserRole.questioner)
    return await show_problem_add_test_case_form(problem_id, request, db)

