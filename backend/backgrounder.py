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
from celery.signals import celeryd_init

# 本项目
from env import REDIS_URL, NODE_ID, DATABASE_URL
from utils.security import sync_load_key_pair
from utils.init import init_node
from utils.model.orm import NodeType
from utils.logger import logger

# 其它库
import time
import uuid

private_key, public_key = sync_load_key_pair()
worker_info_dict = {
    'node_id': NODE_ID,
    'private_key': private_key,
    'public_key': public_key
}

app = Celery("mossy", broker=REDIS_URL, backend='db+'+DATABASE_URL)
app.conf.update(
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
)
app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
app.conf.redbeat_redis_url = REDIS_URL
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'
app.conf.enable_utc = True
