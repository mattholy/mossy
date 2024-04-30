# -*- encoding: utf-8 -*-
'''
endpoint.py
----
support nodeinfo


@Time    :   2024/04/30 14:19:52
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from env import BACKEND_URL

router = APIRouter(prefix='/nodeinfo', tags=['Nodeinfo'])


class NodeInfo(BaseModel):
    links: List['NodeinfoLinks']


class NodeinfoLinks(BaseModel):
    rel: str
    href: str


@router.get('/', response_model=NodeInfo)
async def nodeinfo():
    return NodeInfo(links=[
        NodeinfoLinks(
            rel='http://nodeinfo.diaspora.software/ns/schema/2.1', href=f'{BACKEND_URL}/nodeinfo/2.1'),
        NodeinfoLinks(
            rel='http://nodeinfo.diaspora.software/ns/schema/2.0', href=f'{BACKEND_URL}/nodeinfo/2.0')
    ])
