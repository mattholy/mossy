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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from env import DATABASE_URL


# 创建 SQLAlchemy 引擎，针对 PostgreSQL 的配置
engine = create_engine(
    DATABASE_URL,
    # echo=True,  # 设置为True以便在开发中查看SQL输出
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

# 提供一个依赖注入用的会话获取器函数


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
