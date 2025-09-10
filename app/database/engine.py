from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)