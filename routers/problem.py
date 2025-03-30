from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.problem import Problem
from models.challenge import Challenge
from dbcon import get_db
from fastapi.templating import Jinja2Templates

problem_router = APIRouter(prefix="/problems", tags=["problems"])
templates = Jinja2Templates(directory="frontend/main/questioner")

def verify_challenge_exists(challenge_id: int, db: AsyncSession):
    result = db.execute(select(Challenge).where(Challenge.id == challenge_id))
    challenge = result.scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

@problem_router.post("/")
async def create_problem(
    challenge_id: int,
    title: str,
    problem_definition: str,
    input_format: str,
    output_format: str,
    db: AsyncSession = Depends(get_db)
):
    verify_challenge_exists(challenge_id, db)
    new_problem = Problem(
        challenge_id=challenge_id,
        title=title,
        problem_definition=problem_definition,
        input_format=input_format,
        output_format=output_format
    )
    db.add(new_problem)
    await db.commit()
    return {"id": new_problem.id, "title": new_problem.title}

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