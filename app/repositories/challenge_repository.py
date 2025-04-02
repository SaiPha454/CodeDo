from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from repositories.challenge_model import Challenge
from repositories.problem_model import Problem

class ChallengeRepository:
    @staticmethod
    async def get_challenges_by_user(user_id: int, db: AsyncSession):
        result = await db.execute(select(Challenge).where(Challenge.created_by == user_id))
        return result.scalars().all()

    @staticmethod
    async def get_challenge_by_id(challenge_id: int, db: AsyncSession):
        result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
        return result.scalar_one_or_none()