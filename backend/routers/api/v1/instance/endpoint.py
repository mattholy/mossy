# -*- encoding: utf-8 -*-
'''
endpoint.py
----
Instance v1 api endpoint


@Time    :   2024/05/07 13:26:26
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from utils.model.instance import InstanceV1
from env import RP_ID, RELEASE_VERSION
from utils.model.orm import SystemConfig
from utils.db import get_db
from utils.tools import get_value_or_default
from utils.logger import logger

router = APIRouter(prefix='/instance',
                   tags=['API', 'v1', 'Mastodon-Compatible'])


@router.get(
    '',
    deprecated=True,
    response_class=JSONResponse,
    response_model=InstanceV1
)
async def fetch_instance(db: AsyncSession = Depends(get_db)):
    '''
    Fetch instance information
    '''
    keys_to_fetch = [
        'server_name',
        'server_desc',
        'server_banner'
    ]
    query = select(SystemConfig).filter(SystemConfig.key.in_(keys_to_fetch))
    results = await db.execute(query)
    config_dict = {result.key: result.value for result in results.scalars()}
    logger.debug(config_dict)
    instance = InstanceV1(
        uri=RP_ID,
        title=get_value_or_default(config_dict.get(
            'server_name'), 'Default Server Name'),
        short_description=get_value_or_default(
            config_dict.get('server_name'), 'Default Server Description'),
        description="",
        email="",
        version=RELEASE_VERSION,
        urls=None,
        stats={
            'user_count': 0,
            'status_count': 0,
            'domain_count': 0
        },
        thumbnail=get_value_or_default(config_dict.get('server_banner'), ''),
        languages=[],
        registrations=True,
        approval_required=False,
        invites_enabled=True,
        configuration={
            "accounts": {
                "max_featured_tags": 10
            },
            "statuses": {
                "max_characters": 10000,
                "max_media_attachments": 10000,
                "characters_reserved_per_url": 23
            },
            "media_attachments": {
                "supported_mime_types": [
                    "image/*",
                    "video/*",
                    "audio/*",
                ],
                "image_size_limit": 16777216,
                "image_matrix_limit": 33177600,
                "video_size_limit": 103809024,
                "video_frame_rate_limit": 120,
                "video_matrix_limit": 8294400
            },
            "polls": {
                "max_options": 16,
                "max_characters_per_option": 100,
                "min_expiration": 300,
                "max_expiration": 2629746
            }
        },
        contact_account={},
        rules=[]
    )
    return instance
