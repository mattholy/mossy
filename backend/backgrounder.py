# -*- encoding: utf-8 -*-
'''
backgrounder.py
----
处理请求-响应链路以外的后台任务


@Time    :   2024/04/16 10:46:24
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

# Celery相关
from celery import Celery
from celery import current_app
from celery.signals import worker_init

# 本项目
from env import REDIS_URL, NODE_ID
from utils.security import sync_load_key_pair
from utils.init import init_node
from utils.model.orm import NodeType
from utils.logger import logger

# 其它库
import time
import uuid

worker_info_dict = {
    'node_id': NODE_ID
}

app = Celery("mossy", broker=REDIS_URL, backend=REDIS_URL)
app.conf.update(
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
)


@worker_init.connect
def configure_worker(sender, **kwargs):
    worker_id = str(uuid.uuid4())
    logger.info(f"Starting Celery worker: {worker_id}@{NODE_ID}")
    worker_info_dict['worker_id'] = worker_id
    private_key, public_key = sync_load_key_pair()
    worker_info_dict['private_key'] = private_key
    worker_info_dict['public_key'] = public_key
    init_node(
        public_key,
        NodeType.backgrounder,
        str(sender)
    )


@app.task
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y
