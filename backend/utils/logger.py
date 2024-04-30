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
from sqlalchemy.ext.asyncio import AsyncSession
from env import RUNTIME
from utils.db import SessionLocal, AsyncSessionLocal
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


async def async_log_error_to_db(exception, node_id: str, worker_id: str) -> str:
    async with AsyncSessionLocal() as db_session:
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
            await db_session.commit()
            return error_uuid
        except Exception as e:
            await db_session.rollback()
            logger.critical(
                f"Failed to log error {error_uuid} to database: {str(e)}",
                exc_info=True
            )
            return error_uuid


def sync_log_error_to_db(exception, node_id: str, worker_id: str):
    db_session: Session = SessionLocal()
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
        db_session.rollback()
        logger.critical(
            f"Failed to log error {error_uuid} to database: {str(e)}")
    finally:
        db_session.close()
        return error_uuid


def operation_log_to_db(
        module: str,
        operation: dict,
        user: str = None,
        related_session: str = None,
) -> bool:
    db_session: Session = SessionLocal()
    try:
        operation_log = OperationLog(
            module=module,
            operation=operation,
            user=user,
            related_session=related_session
        )

        db_session.add(operation_log)
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.critical(
            f"Failed to log operation {operation} to database: {str(e)}",
            exc_info=True
        )
        return False
    finally:
        db_session.close()


async def async_operation_log_to_db(
        module: str,
        operation: dict,
        user: str = None,
        related_session: str = None,
) -> bool:
    async with AsyncSessionLocal() as db_session:
        try:
            operation_log = OperationLog(
                module=module,
                operation=operation,
                user=user,
                related_session=related_session
            )

            db_session.add(operation_log)
            await db_session.commit()
            return True
        except Exception as e:
            await db_session.rollback()
            logger.critical(
                f"Failed to log operation {operation} to database: {str(e)}",
                exc_info=True
            )
            return False
