from fastapi import APIRouter, Depends, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from services.questioner_problem_service import QuestionerProblemService
from config.dbcon import get_db
from routers import questioner_testcase_router
from services.questioner_challenge_service import QuestionerChallengeService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_problems(challenge_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    problems = await QuestionerProblemService.get_problems(challenge_id, db)
    challenge = await QuestionerChallengeService.get_challenge(challenge_id, db)
    return templates.TemplateResponse(
        "/questioner/problem_dashboard.html", {"request": request, "problems": problems, "challenge": challenge}
    )

@router.post("/")
async def create_problem(
    challenge_id: int,
    title: str = Body(...),
    problem_definition: str = Body(...),
    input_format: str = Body(...),
    output_format: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    await QuestionerProblemService.create_problem(challenge_id, title, problem_definition, input_format, output_format, db)
    return RedirectResponse(url=f"/questioners/challenges/{challenge_id}/problems", status_code=303)

@router.get("/{id}/")
async def get_problem(id: int, db: AsyncSession = Depends(get_db)):
    return await QuestionerProblemService.get_problem(id, db)

@router.get("/new")
async def show_problem_creation_form(challenge_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    challenge = await QuestionerChallengeService.get_challenge(challenge_id, db)
    return templates.TemplateResponse(
        "questioner/problem_creation_form.html", {"request": request, "challenge": challenge}
    )

@router.delete("/{problem_id}/")
async def delete_problem_route(problem_id: int, challenge_id: int, db: AsyncSession = Depends(get_db)):
    await QuestionerProblemService.delete_problem(problem_id, db)
    return RedirectResponse(url=f"/questioners/challenges/{challenge_id}/problems", status_code=303)

@router.get("/{problem_id}/edit")
async def show_problem_edit_form(
    challenge_id: int,
    problem_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    challenge = await QuestionerChallengeService.get_challenge(challenge_id, db)
    problem = await QuestionerProblemService.get_problem(problem_id, db)
    problem.problem_definition = problem.problem_definition.replace("\\n", "\n")
    problem.input_format = problem.input_format.replace("\\n", "\n")
    problem.output_format = problem.output_format.replace("\\n", "\n")
    return templates.TemplateResponse(
        "questioner/problem_edit_form.html", {"request": request, "problem": problem, "challenge": challenge}
    )

@router.put("/{problem_id}/")
async def update_problem_route(
    problem_id: int,
    title: str = Body(...),
    problem_definition: str = Body(...),
    input_format: str = Body(...),
    output_format: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    await QuestionerProblemService.update_problem(problem_id, title, problem_definition, input_format, output_format, db)
    return RedirectResponse(url=f"/questioners/challenges/{problem_id}/problems", status_code=303)

# @router.get("/{problem_id}/testcases")
# async def show_problem_add_test_case_form(
#     problem_id: int,
#     request: Request,
#     db: AsyncSession = Depends(get_db)
# ):
#     test_cases = await QuestionerProblemService.get_test_cases(problem_id, db)
#     problem = await QuestionerProblemService.get_problem(problem_id, db)
#     return templates.TemplateResponse(
#         "questioner/testcase_form.html", {
#             "request": request,
#             "problem": problem,
#             "test_cases": test_cases
#         }
#     )

router.include_router(questioner_testcase_router.router, prefix="/{problem_id}/testcases", tags=["testcases"])