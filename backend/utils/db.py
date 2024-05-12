# -*- encoding: utf-8 -*-
'''
db.py
----
数据库连接池


@Time    :   2024/04/13 17:31:30
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from env import DATABASE_URL, RUNTIME


engine = create_engine(
    DATABASE_URL,
    # echo=True if RUNTIME == 'DEV' else False,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    # echo=True if RUNTIME == 'DEV' else False,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
