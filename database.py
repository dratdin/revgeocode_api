from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


db_engine = create_async_engine(
    "sqlite+aiosqlite:///geocoding.db"
)
db_session = async_sessionmaker(db_engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


async def create_tables():
    async with db_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_tables():
    async with db_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
