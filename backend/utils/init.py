# -*- encoding: utf-8 -*-
'''
init.py
----
put some words here


@Time    :   2024/04/25 17:10:24
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from utils.db import SessionLocal
from utils.model.orm import NodeInfo
from utils.model.orm import NodeType
from env import NODE_ID, IPV6S, IPV4S

import multiprocessing
import platform
import psutil


def init_node(public_key: str, type: NodeType, remark: str = None, status: bool = True):
    with SessionLocal() as db:
        node = db.query(NodeInfo).filter_by(
            node_id=NODE_ID, node_type=type).first()
        if not node:
            node = NodeInfo(
                node_id=NODE_ID,
                node_type=type,
                cpus=get_cpu_cores(),
                mem_in_gb=get_memory_gb(),
                node_name=get_hostname(),
                ipv4=','.join(IPV4S),
                ipv6=','.join(IPV6S),
                public_key=public_key,
                remark=remark
            )
            db.add(node)
        else:
            node.cpus = get_cpu_cores()
            node.mem_in_gb = get_memory_gb()
            node.node_name = get_hostname()
            node.ipv4 = ','.join(IPV4S)
            node.ipv6 = ','.join(IPV6S)
            node.remark = remark
            node.activated = status
        db.commit()


def get_cpu_cores():
    return multiprocessing.cpu_count()


def get_memory_gb():
    mem_info = psutil.virtual_memory()
    mem_total_gb = mem_info.total / 1024 / 1024 / 1024
    return mem_total_gb


def get_hostname():
    return platform.node()
