# -*- encoding: utf-8 -*-
'''
router.py
----
put some words here


@Time    :   2024/05/14 23:36:40
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''


from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, HttpUrl
from typing import Optional

from env import RP_ID, RELEASE_VERSION
from utils.model.orm import SystemConfig
from utils.db import get_db
from utils.tools import get_value_or_default
from utils.logger import logger
from utils.system.security import get_current_user

router = APIRouter(prefix='/oauth', tags=['OAuth'])


@app.get('/authorize')
async def authorize(request: Request, user_id: int = Depends(get_current_user)):
    user = {'id': user_id}
    return await authorization.create_authorization_response(request, grant_user=user)


@router.post('/token')
async def token():
    return {
        "access_token": "raOShq-qMOpH2FXMtJZbrZmiuFsUbvCoUhv2CrqsjPo"
    }
