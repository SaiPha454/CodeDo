from fastapi import APIRouter, HTTPException, Depends, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.problem import Problem
from models.challenge import Challenge
from models.test_case import TestCase
from dbcon import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
problem_router = APIRouter(prefix="/problems", tags=["problems"])
templates = Jinja2Templates(directory="frontend/main/questioner")

async def verify_challenge_exists(challenge_id: int, db: AsyncSession):
    result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
    challenge = result.scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

@problem_router.post("/")
async def create_problem(
    challenge_id: int = Body(...),
    title: str = Body(...),
    problem_definition: str = Body(...),
    input_format: str = Body(...),
    output_format: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    await verify_challenge_exists(challenge_id, db)
    new_problem = Problem(
        challenge_id=challenge_id,
        title=title,
        problem_definition=problem_definition,
        input_format=input_format,
        output_format=output_format
    )
    db.add(new_problem)
    await db.commit()
    return RedirectResponse(url=f"/questioners/challenges/{challenge_id}/problems", status_code=303)

@problem_router.get("/{id}/")
async def get_problem(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Problem).where(Problem.id == id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@problem_router.get("/challenges/{challenge_id}/problems")
async def list_problems_for_challenge(challenge_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    # Fetch problems associated with the given challenge_id
    result = await db.execute(select(Problem).where(Problem.challenge_id == challenge_id))
    problems = result.scalars().all()
    # Render the problem dashboard template
    return templates.TemplateResponse(
        "problem_dashboard.html", {"request": request, "problems": problems, "challenge_id": challenge_id}
    )

@problem_router.get("/challenges/{challenge_id}/problems/new")
async def show_problem_creation_form(challenge_id: int, request: Request):
    return templates.TemplateResponse(
        "problem_creation_form.html", {"request": request, "challenge_id": challenge_id}
    )

@problem_router.delete("/{problem_id}/")
async def delete_problem_route(problem_id: int, challenge_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch the problem to ensure it exists
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Delete the problem
    await db.delete(problem)
    await db.commit()

    # Redirect to the updated problems list
    return RedirectResponse(url=f"/questioners/challenges/{challenge_id}/problems", status_code=303)

@problem_router.get("/{problem_id}/edit")
async def show_problem_edit_form(
    challenge_id: int,
    problem_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the problem to edit
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Format \n to actual newlines for display in the form
    problem.problem_definition = problem.problem_definition.replace("\\n", "\n")
    problem.input_format = problem.input_format.replace("\\n", "\n")
    problem.output_format = problem.output_format.replace("\\n", "\n")

    # Render the edit form
    return templates.TemplateResponse(
        "problem_edit_form.html", {"request": request, "problem": problem, "challenge_id": challenge_id}
    )

@problem_router.put("/{problem_id}/")
async def update_problem_route(
    problem_id: int,
    title: str = Body(...),
    problem_definition: str = Body(...),
    input_format: str = Body(...),
    output_format: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    # Fetch the problem to ensure it exists
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Update the problem fields
    problem.title = title
    problem.problem_definition = problem_definition
    problem.input_format = input_format
    problem.output_format = output_format

    # Commit the changes
    await db.commit()

    # Redirect to the updated problems list
    return RedirectResponse(url=f"/questioners/challenges/{problem.challenge_id}/problems", status_code=303)

@problem_router.get("/{problem_id}/testcases")
async def show_problem_add_test_case_form(
    challenge_id: int,
    problem_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the problem to edit
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Fetch associated test cases
    test_case_result = await db.execute(select(TestCase).where(TestCase.problem_id == problem_id))
    test_cases = test_case_result.scalars().all()
    for test_case in test_cases:
        # Deserialize input_data from JSON string to list
        test_case.input_data = json.loads(test_case.input_data)
        print(test_case.input_data)
    
    # Render the test case form with test cases
    return templates.TemplateResponse(
        "test_case_form.html", {
            "request": request,
            "problem": problem,
            "challenge_id": challenge_id,
            "test_cases": test_cases
        }
    )