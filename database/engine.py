from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker,create_async_engine

from database.models import Base

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3',echo = True)

async_sessionmaker = async_sessionmaker(engine)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
