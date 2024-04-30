# -*- encoding: utf-8 -*-
'''
logger.py
----
一个简单的日志模块


@Time    :   2024/04/15 14:26:47
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import logging
import traceback
import uuid
from colorlog import ColoredFormatter

from sqlalchemy.orm import Session
from env import RUNTIME
from utils.db import SessionLocal
from utils.model.orm import ErrorLog, OperationLog


logger = logging.getLogger()
logger.setLevel(logging.DEBUG if RUNTIME == 'DEV' else logging.INFO)


handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(asctime)s - %(log_color)s%(levelname)s%(reset)s - [%(pathname)s:%(lineno)d] : "
    "%(message_log_color)s%(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'bold_red',
        'CRITICAL': 'bold_red',
    },
    secondary_log_colors={
        'message': {
            'CRITICAL': 'bold'
        }
    },
    style='%'
)

handler.setFormatter(formatter)
logger.addHandler(handler)


def log_error_to_db(exception, node_id: str, worker_id: str):
    db_session = SessionLocal()
    try:
        error_uuid = str(uuid.uuid4())
        error_message = str(exception)
        error_type = type(exception).__name__
        error_stack = "".join(traceback.format_exception(
            None, exception, exception.__traceback__))

        error_log = ErrorLog(
            id=error_uuid,
            node_id=node_id,
            worker_id=worker_id,
            error_message=error_message,
            error_type=error_type,
            error_stack=error_stack
        )
        db_session.add(error_log)
        db_session.commit()
    except Exception as e:
        db_session.rollback()  # 确保在出错时回滚
        logger.critical(
            f"Failed to log error {error_uuid} to database: {str(e)}")
    finally:
        db_session.close()
        return error_uuid


def operation_log_to_db():
    db_session = SessionLocal()
    pass
