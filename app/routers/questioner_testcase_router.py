from fastapi import APIRouter, HTTPException, Depends, Request, Body
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from services.questioner_challenge_service import QuestionerChallengeService

from repositories.test_case_model import TestCase
from config.dbcon import get_db
from services.questioner_problem_service import QuestionerProblemService

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def show_problem_add_test_case_form(
    challenge_id: int,
    problem_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    test_cases = await QuestionerProblemService.get_test_cases(problem_id, db)
    problem = await QuestionerProblemService.get_problem(problem_id, db)
    challenge = await QuestionerChallengeService.get_challenge(challenge_id, db)
    return templates.TemplateResponse(
        "questioner/testcase_form.html", {
            "request": request,
            "problem": problem,
            "test_cases": test_cases,
            'challenge':challenge
        }
    )

@router.post("/", response_class=HTMLResponse)
async def update_test_cases(
    request: Request,
    challenge_id: int,
    problem_id: int,
    test_cases: list[dict] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    # Delete all existing test cases for the problem using SQLAlchemy ORM
    await db.execute(
        delete(TestCase).where(TestCase.problem_id == problem_id)
    )

    # Insert new test cases with sequential IDs
    for index, test_case_data in enumerate(test_cases, start=1):
        new_test_case = TestCase(
            problem_id=problem_id,
            id=index,  # Assign sequential IDs starting from 1
            input_data=test_case_data["input_data"],  # Serialize list to string
            expected_output=test_case_data["expected_output"]
        )
        db.add(new_test_case)

    # Commit changes
    await db.commit()

    # Fetch updated test cases
    return  RedirectResponse(
        url=f"/questioners/challenges/{challenge_id}/problems/",
        status_code=303
    )