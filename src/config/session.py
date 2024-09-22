from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config.settings import config

engine = create_async_engine(config.database.database_url, echo=True, future=True)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для получения асинхронного сеанса"""
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        await session.close()
