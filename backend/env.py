# -*- encoding: utf-8 -*-
'''
env.py
----
设置环境


@Time    :   2024/04/12 16:47:06
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import os
import uuid
import socket
import netifaces
from urllib.parse import urlparse
from functools import cache


@cache
def is_physical_interface(interface_name):
    # 这里列出一些常见的虚拟接口前缀，根据实际情况可能需要调整
    virtual_prefixes = ('lo', 'docker', 'vmnet',
                        'vboxnet', 'tun', 'tap', 'virbr')
    return not any(interface_name.startswith(prefix) for prefix in virtual_prefixes)


@cache
def get_physical_ips():
    ipv4_addresses = []
    ipv6_addresses = []
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        if is_physical_interface(interface):
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                # IPv4
                for link in addrs[netifaces.AF_INET]:
                    ipv4_addresses.append(link['addr'])
            if netifaces.AF_INET6 in addrs:
                # IPv6
                for link in addrs[netifaces.AF_INET6]:
                    ipv6_addresses.append(link['addr'])

    return ipv4_addresses, ipv6_addresses


IPV4S, IPV6S = get_physical_ips()


@cache
def generate_uuid_from_ip():
    try:
        IPV4S, IPV6S = get_physical_ips()
        namespace = uuid.NAMESPACE_DNS
        t_uuid = str(uuid.uuid5(namespace, IPV4S[0]))
        return t_uuid
    except:
        return '00000000-0000-0000-0000-000000000000'


BACKEND_URL = os.environ.get('CLUSTER_ID', 'http://localhost:8000')
RELEASE_VERSION = os.environ.get('RELEASE_TAG', 'dev')
API_BASE_URL = '/api'

RP_SOURCE = os.environ.get('CLUSTER_ID', 'http://localhost:5173')
RP_ID = urlparse(RP_SOURCE).hostname
RP_NAME = 'Mossy'

DATABASE_URL = os.environ.get(
    'DATABASE_URL', 'postgresql://username:password@localhost:5432/dbname')

REDIS_URL = os.environ.get(
    'REDIS_URL', 'redis://:password@localhost:6379/0')

RUNTIME = os.environ.get('RUNTIME', 'DEV')

NODE_ID = os.environ.get(
    'NODE_ID', generate_uuid_from_ip())

ACTIVITYPUB_ID = os.environ.get('CLUSTER_ID', 'http://localhost:5173')
