from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class UserService:
    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession):
        
        user= await UserRepository.get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    