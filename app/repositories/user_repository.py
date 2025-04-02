from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from repositories.user_model import User, UserRole
import bcrypt

class UserRepository:
    @staticmethod
    async def create_user(username: str, email: str, password: str, role: UserRole, db: AsyncSession):
        try:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            print(f"Hashed password: {hashed_password}", role, username, email)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password.decode("utf-8"),
                role=role
            )
            db.add(new_user)
            await db.commit()
            return new_user.id
        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Signup failed. Please try again.")

    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()