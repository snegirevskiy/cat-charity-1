from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.core.base import Base # noqa

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
