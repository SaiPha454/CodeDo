from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://codedo:codedo42@localhost:5432/codedodb"

# Create the SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
