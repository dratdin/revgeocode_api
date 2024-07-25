from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


DB = "sqlite+aiosqlite:///geocoding.db"

async_db_engine = create_async_engine(DB)

async_db_session = async_sessionmaker(async_db_engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


async def create_tables():
    async with async_db_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_tables():
    async with async_db_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
