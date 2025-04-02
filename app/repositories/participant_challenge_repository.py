from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from sqlalchemy.orm import selectinload
from repositories.challenge_model import Challenge
from repositories.problem_model import Problem
from repositories.challenge_repository import ChallengeRepository
from repositories.participant_challenge_model import ParticipantChallenge

class ParticipantChallengeRepository(ChallengeRepository):
    @staticmethod
    async def add_participant_to_challenge(participant_id: int, challenge_id: int, db: AsyncSession):
        try:
            participant_challenge = ParticipantChallenge(
                participant_id=participant_id,
                challenge_id=challenge_id
            )
            db.add(participant_challenge)
            await db.commit()
            return participant_challenge
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def is_participant_in_challenge(participant_id: int, challenge_id: int, db: AsyncSession):
        result = await db.execute(
            select(ParticipantChallenge).where(
                ParticipantChallenge.participant_id == participant_id,
                ParticipantChallenge.challenge_id == challenge_id
            )
        )
        return result.scalars().first() is not None

    @staticmethod
    async def get_challenges_by_participant(participant_id: int, db: AsyncSession):
        result = await db.execute(
            select(ParticipantChallenge, Challenge)
            .join(Challenge, ParticipantChallenge.challenge_id == Challenge.id)
            .where(ParticipantChallenge.participant_id == participant_id)
            .options(selectinload(Challenge.problems))  # Load problems relationship
        )
        return result.all()

    @staticmethod
    async def delete_participant_from_challenge(participant_id: int, challenge_id: int, db: AsyncSession):
        try:
            await db.execute(
                delete(ParticipantChallenge).where(
                    ParticipantChallenge.participant_id == participant_id,
                    ParticipantChallenge.challenge_id == challenge_id
                )
            )
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_challenge_with_problems(challenge_id: int, db: AsyncSession):
        result = await db.execute(
            select(Challenge)
            .where(Challenge.id == challenge_id)
            .options(selectinload(Challenge.problems))  # Load problems relationship
        )
        return result.scalars().first()