from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from repositories.test_case_model import TestCase

class ParticipantTestCaseRepository:
    
    @staticmethod
    async def get_first_two_test_cases(problem_id: int, db: AsyncSession):
        result = await db.execute(
            select(TestCase)
            .where(TestCase.problem_id == problem_id)
            .limit(2)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_test_cases(problem_id: int, db: AsyncSession):
        result = await db.execute(
            select(TestCase).where(TestCase.problem_id == problem_id)
        )
        return result.scalars().all()