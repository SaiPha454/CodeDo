from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_model import UserRole
from repositories.user_repository import UserRepository
import bcrypt

class AuthLogic:
    @staticmethod
    async def signup(username: str, email: str, password: str, role: str, db: AsyncSession):
        role_enum = UserRole(role)
        return await UserRepository.create_user(username, email, password, role_enum, db)

    @staticmethod
    async def login(email: str, password: str, db: AsyncSession):
        user = await UserRepository.get_user_by_email(email, db)
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return user.id, user.role.value
        raise HTTPException(status_code=401, detail="Invalid credentials")

    @staticmethod
    async def setup_session(request: Request, user_id: int, role: str):
        request.session["user_id"] = user_id
        request.session["role"] = role

    @staticmethod
    async def redirect_based_on_role(role: str):
        if role == UserRole.participant.value:
            return RedirectResponse(url="/participants/dashboard", status_code=302)
        elif role == UserRole.questioner.value:
            return RedirectResponse(url="/questioners/challenges", status_code=302)
    @staticmethod
    async def get_current_user(request: Request, db: AsyncSession):
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Not authenticated")
        user = await UserRepository.get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user