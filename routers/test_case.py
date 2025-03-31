from fastapi import APIRouter, HTTPException, Depends, Request, Body
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from models.test_case import TestCase
from dbcon import get_db
import json
from routers.problem import show_problem_add_test_case_form

templates = Jinja2Templates(directory="frontend/main/questioner")

test_case_router = APIRouter(prefix="/test_cases", tags=["test_cases"])

@test_case_router.post("/", response_class=HTMLResponse)
async def update_test_cases(
    request: Request,
    problem_id: int = Body(...),
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
            input_data=json.dumps(test_case_data["parameters"]),  # Serialize list to string
            expected_output=test_case_data["expected_output"]
        )
        db.add(new_test_case)

    # Commit changes
    await db.commit()

    # Fetch updated test cases
    return  RedirectResponse(
        url=f"/questioners/problems/{problem_id}/testcases",
        status_code=303
    )