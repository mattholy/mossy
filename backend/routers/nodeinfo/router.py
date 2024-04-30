# -*- encoding: utf-8 -*-
'''
router.py
----
router for nodeinfo endpoints


@Time    :   2024/04/30 15:04:05
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter, Response
from utils.model.nodeinfo import NodeInfo2dot1, NodeInfo2dot0
from env import RELEASE_VERSION

router = APIRouter(prefix='/nodeinfo', tags=['Nodeinfo'])


@router.get('/2.1', response_model=NodeInfo2dot1)
async def fetch_nodeinfo_v2_1(response: Response):
    response.headers['Content-Type'] = 'application/json; profile="http://nodeinfo.diaspora.software/ns/schema/2.1#"; charset=utf-8'
    return NodeInfo2dot1(
        software={
            'name': 'mossy',
            'version': RELEASE_VERSION,
            'homepage': 'https://github.com/mattholy/mossy',
            'repository': 'https://github.com/mattholy/mossy',
        },
        protocols=['activitypub'],
        services={
            'inbound': [],
            'outbound': []
        },
        openRegistrations=True,
        usage={
            'users': {
                'total': 0,
                'activeHalfyear': 0,
                'activeMonth': 0
            },
            'localPosts': 0,
            'localComments': 0
        },
        metadata={}
    )


@router.get('/2.0', response_model=NodeInfo2dot0)
async def fetch_nodeinfo_v2_0(response: Response):
    response.headers['Content-Type'] = 'application/json; profile="http://nodeinfo.diaspora.software/ns/schema/2.0#"; charset=utf-8'
    return NodeInfo2dot0(
        software={
            'name': 'mossy',
            'version': RELEASE_VERSION
        },
        protocols=['activitypub'],
        services={
            'inbound': [],
            'outbound': []
        },
        open_registrations=True,
        usage={
            'users': {
                'total': 0,
                'activeHalfyear': 0,
                'activeMonth': 0
            },
            'localPosts': 0,
            'localComments': 0
        },
        metadata={}
    )
