from repositories.questioner_challenge_repository import QuestionerChallengeRepository
from repositories.user_model import UserRole
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

class QuestionerChallengeService:
    @staticmethod
    async def display_challenges(request: Request, db: AsyncSession):
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        challenges = await QuestionerChallengeRepository.get_challenges_by_user(user_id, db)
        for challenge in challenges:
            challenge.created_at = challenge.created_at.strftime("%B %d, %Y %I:%M %p")
        return challenges

    @staticmethod
    async def create_challenge(request: Request, title: str, db: AsyncSession):
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return await QuestionerChallengeRepository.create_challenge(title, user_id, db)

    @staticmethod
    async def get_challenge(challenge_id: int, db: AsyncSession):
        challenge = await QuestionerChallengeRepository.get_challenge_by_id(challenge_id, db)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        return challenge

    @staticmethod
    async def delete_challenge(request: Request, challenge_id: int, db: AsyncSession):
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        challenge = await QuestionerChallengeRepository.delete_challenge(challenge_id, user_id, db)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found or not authorized to delete")
        return await QuestionerChallengeRepository.get_challenges_by_user(user_id, db)