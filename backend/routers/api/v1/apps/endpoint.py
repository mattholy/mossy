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

import uuid
from fastapi import APIRouter, Depends, Query, Body
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

from utils.model.instance import InstanceV1
from env import RP_ID, RELEASE_VERSION
from utils.model.orm import SystemConfig, OAuthApp
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
    client_id: Optional[uuid.UUID] = None
    client_secret: Optional[str] = None


class AppOauthData(BaseModel):
    client_name: str
    redirect_uris: str
    scopes: str
    website: str


async def get_payload(
    client_name: Optional[str] = Query(None),
    website: Optional[str] = Query(None),
    redirect_uris: Optional[str] = Query(None),
    scopes: Optional[str] = Query(None),
    body: Optional[AppOauthData] = Body(None)
):
    if body:
        return body
    elif all([client_name, website, redirect_uris, scopes]):
        return AppOauthData(
            client_name=client_name,
            website=website,
            redirect_uris=redirect_uris,
            scopes=scopes
        )
    else:
        raise HTTPException(status_code=422, detail="InvalidParameters")


@router.post(
    '',
    response_class=JSONResponse,
    response_model=AppModel,
    tags=['OAuth']
)
async def app_register(
    payload: AppOauthData = Depends(get_payload),
    db: AsyncSession = Depends(get_db)
):
    new_app = OAuthApp(
        name=payload.client_name,
        website=payload.website,
        redirect_uri=payload.redirect_uris,
        scopes=payload.scopes
    )
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return AppModel(
        id=str(new_app.id),
        name=new_app.name,
        website=new_app.website,
        redirect_uri=new_app.redirect_uri,
        client_id=new_app.client_id,
        client_secret=new_app.client_secret
    )
