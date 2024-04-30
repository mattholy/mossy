#!/bin/bash

# 执行数据库迁移
poetry run alembic upgrade head

# 设置默认工作进程数
if [ -z "$WORKERS" ]; then
    WORKERS=$((2 * $(nproc) + 1))
fi

# 根据 RUNTIME 设置日志级别
if [ "$RUNTIME" = "PRO" ]; then
    LOG_LEVEL="info"
else
    LOG_LEVEL="debug"
fi

# 导出日志级别环境变量，供 supervisord 和其他程序使用
export LOG_LEVEL

# 根据 SERVICE_MODE 环境变量决定操作
case $SERVICE_MODE in
  web)
    # 仅启动 FastAPI 应用
    exec poetry run gunicorn -w $WORKERS -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --log-level=$LOG_LEVEL --access-logfile - --access-logformat "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s'"
    ;;
  backgrounder)
    # 仅启动 Celery Worker
    exec poetry run celery -A backgrounder worker --loglevel=$LOG_LEVEL -c $WORKERS
    ;;
  scheduler)
    # 仅启动 Celery Scheduler
    exec poetry run celery -A backgrounder beat --loglevel=$LOG_LEVEL
    ;;
  *)
    # 启动 supervisord 来同时管理 FastAPI 和 Celery Worker
    exec poetry run supervisord -c ./supervisord.conf
    ;;
esac
