from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from repositories.problem_model import Problem
from repositories.test_case_model import TestCase
import json

class QuestionerProblemRepository:
    @staticmethod
    async def get_problems_by_challenge_id(challenge_id: int, db: AsyncSession):
        result = await db.execute(select(Problem).where(Problem.challenge_id == challenge_id))
        return result.scalars().all()

    @staticmethod
    async def create_problem(challenge_id: int, title: str, problem_definition: str, input_format: str, output_format: str, db: AsyncSession):
        new_problem = Problem(
            challenge_id=challenge_id,
            title=title,
            problem_definition=problem_definition,
            input_format=input_format,
            output_format=output_format
        )
        db.add(new_problem)
        await db.commit()
        return new_problem

    @staticmethod
    async def get_problem_by_id(problem_id: int, db: AsyncSession):
        result = await db.execute(select(Problem).where(Problem.id == problem_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_problem(problem_id: int, title: str, problem_definition: str, input_format: str, output_format: str, db: AsyncSession):
        problem = await QuestionerProblemRepository.get_problem_by_id(problem_id, db)
        if problem:
            problem.title = title
            problem.problem_definition = problem_definition
            problem.input_format = input_format
            problem.output_format = output_format
            await db.commit()
        return problem

    @staticmethod
    async def delete_problem(problem_id: int, db: AsyncSession):
        problem = await QuestionerProblemRepository.get_problem_by_id(problem_id, db)
        if problem:
            await db.delete(problem)
            await db.commit()
        return problem

    @staticmethod
    async def get_test_cases_by_problem_id(problem_id: int, db: AsyncSession):
        result = await db.execute(select(TestCase).where(TestCase.problem_id == problem_id))
        test_cases = result.scalars().all()
        for test_case in test_cases:
            test_case.input_data = json.loads(test_case.input_data)
        return test_cases