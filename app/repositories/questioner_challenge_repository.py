from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from repositories.challenge_model import Challenge
from repositories.problem_model import Problem
from repositories.challenge_repository import ChallengeRepository
class QuestionerChallengeRepository(ChallengeRepository):
    # @staticmethod
    # async def get_challenges_by_user(user_id: int, db: AsyncSession):
    #     result = await db.execute(select(Challenge).where(Challenge.created_by == user_id))
    #     return result.scalars().all()

    @staticmethod
    async def create_challenge(title: str, user_id: int, db: AsyncSession):
        new_challenge = Challenge(title=title, created_by=user_id)
        db.add(new_challenge)
        await db.commit()
        return new_challenge

    # @staticmethod
    # async def get_challenge_by_id(challenge_id: int, db: AsyncSession):
    #     result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
    #     return result.scalar_one_or_none()

    @staticmethod
    async def delete_challenge(challenge_id: int, user_id: int, db: AsyncSession):
        # Fetch the challenge
        result = await db.execute(select(Challenge).where(Challenge.id == challenge_id, Challenge.created_by == user_id))
        challenge = result.scalar_one_or_none()
        if not challenge:
            return None

        # Delete associated problems
        await db.execute(
            delete(Problem).where(Problem.challenge_id == challenge_id)
        )

        # Delete the challenge
        await db.delete(challenge)
        await db.commit()
        return challenge