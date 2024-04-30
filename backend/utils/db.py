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


# 创建 SQLAlchemy 引擎，针对 PostgreSQL 的配置
engine = create_engine(
    DATABASE_URL,
    echo=True if RUNTIME == 'DEV' else False,
    pool_size=20,  # 连接池大小
    max_overflow=10,  # 超过连接池大小外最多创建的连接数
    pool_timeout=30,  # 池中没有线程可用时，连接的最大等待时间，单位秒
    pool_recycle=1800,  # 连接最大复用时间，单位秒
)

async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),  # 注意驱动名更改
    echo=True if RUNTIME == 'DEV' else False,
    pool_size=20,  # 连接池大小
    max_overflow=10,  # 超过连接池大小外最多创建的连接数
    pool_timeout=30,  # 池中没有线程可用时，连接的最大等待时间，单位秒
    pool_recycle=1800,  # 连接最大复用时间，单位秒
)

# 创建会话制造器
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

# 提供一个依赖注入用的会话获取器函数


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
