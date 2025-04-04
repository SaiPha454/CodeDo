from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Request
from services.auth_service import AuthLogic
from repositories.user_model import UserRole
class UserService:
    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession):
        
        user= await UserRepository.get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    @staticmethod
    async def update_user_name(request: Request, new_username: str, db: AsyncSession):
        user = await AuthLogic.get_current_user(request=request, db=db)  # Added await to resolve the coroutine
        return await UserRepository.update_user_name(user.id, new_username, db)
       