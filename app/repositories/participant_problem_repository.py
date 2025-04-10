from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from repositories.test_case_model import TestCase
from repositories.problem_model import Problem
class ParticipantProblemRepository:
    @staticmethod
    async def get_first_two_test_cases(problem_id: int, db: AsyncSession):
        result = await db.execute(
            select(TestCase)
            .where(TestCase.problem_id == problem_id)
            .limit(2)
        )
        return result.scalars().all()
    

    @staticmethod
    async def get_problem_by_id(problem_id: int, db: AsyncSession):
        result = await db.execute(
            select(Problem).where(Problem.id == problem_id)
        )
        return result.scalar_one_or_none()