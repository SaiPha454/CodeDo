from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from repositories.user_repository import UserRepository
from repositories.user_model import User, UserRole
from middlewares.role_middleware import RoleMiddleware
from repositories.challenge_model import Challenge
from repositories.participant_challenge_repository import ParticipantChallengeRepository

class JoinChallengeService:

    @staticmethod
    async def validate_user(request: Request, db: AsyncSession):
        user_id = request.session.get("user_id")
        if not user_id:
            return RedirectResponse(url="/login", status_code=302)
        RoleMiddleware.verify_role(request, UserRole.participant)
        user = await UserRepository.get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    @staticmethod
    async def get_challenge(request: Request, challenge_id: int, db: AsyncSession):
        challenge = await ParticipantChallengeRepository.get_challenge_by_id(challenge_id, db)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        return challenge
    
    @staticmethod
    async def join_challenge(request: Request, participant_id: int, challenge_id: int, db: AsyncSession):
        user = await JoinChallengeService.validate_user(request, db)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        # Check if the challenge exists
        challenge = await JoinChallengeService.get_challenge(request, challenge_id, db)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        # Check if the participant is already in the challenge
        already_joined = await ParticipantChallengeRepository.is_participant_in_challenge(participant_id, challenge_id, db)
        if already_joined:
            return RedirectResponse(url="/participants/dashboard", status_code=302)
        particpant_challenge = await ParticipantChallengeRepository.add_participant_to_challenge(participant_id, challenge_id, db)
        if not particpant_challenge:
            raise HTTPException(status_code=400, detail="Failed to join the challenge")
        return RedirectResponse(url="/participants/dashboard", status_code=302)