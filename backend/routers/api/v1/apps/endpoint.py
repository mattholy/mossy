# -*- encoding: utf-8 -*-
'''
endpoint.py
----
put some words here


@Time    :   2024/05/14 22:49:01
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, HttpUrl
from typing import Optional

from utils.model.instance import InstanceV1
from env import RP_ID, RELEASE_VERSION
from utils.model.orm import SystemConfig
from utils.db import get_db
from utils.tools import get_value_or_default
from utils.logger import logger

router = APIRouter(prefix='/apps',
                   tags=['API', 'v1', 'Mastodon-Compatible'])


class AppModel(BaseModel):
    id: str
    name: str
    website: Optional[HttpUrl] = None
    redirect_uri: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    vapid_key: str


@router.post(
    '',
    response_class=JSONResponse,
    response_model=AppModel,
    tags=['OAuth']
)
async def app_register(
        client_name: str,
        redirect_uris: str,
        scopes: Optional[str],
        website: Optional[str],
        db: AsyncSession = Depends(get_db)):
    data = {
        "id": "672",
        "name": "IceCubesApp",
        "website": "https://github.com/Dimillian/IceCubesApp",
        "redirect_uri": "icecubesapp://",
        "client_id": "raOShq-qMOpH2FXMtJZbrZmiuFsUbvCoUhv2CrqsjPo",
        "client_secret": "Am-znehfqmHqSAUuVE3mBYcTAYtak_f8mKBBXXNsnOg",
        "vapid_key": "BKvZCto1H0fjRImRU6qLLzzouE0_Twtwv67fNkXU5PN7lPFkEtwsPT7TOUGr8TuFwUxJah7WSedNgppHlfA2P2k="
    }
    return AppModel(**data)
