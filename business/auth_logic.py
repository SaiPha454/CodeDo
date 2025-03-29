from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from models.user_model import User  # Updated import
import bcrypt

class AuthLogic:
    @staticmethod
    async def signup(username: str, email: str, password: str, db: AsyncSession):
        try:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            new_user = User(username=username, email=email, password=hashed_password.decode("utf-8"))
            db.add(new_user)
            await db.commit()
            return new_user.id
        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Signup failed. Please try again.")

    @staticmethod
    async def login(email: str, password: str, db: AsyncSession):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return user.id
        raise HTTPException(status_code=401, detail="Invalid credentials")
