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
from utils.model.orm import SystemConfig, OAuthAuthorizationCode
from utils.model.api_schemas import BaseApiResp
from utils.db import get_db
from utils.tools import get_value_or_default
from utils.logger import logger, async_operation_log_to_db
from utils.system.security import get_current_user_session, UserSession
from datetime import datetime, timedelta, UTC

router = APIRouter(prefix='/oauth', tags=['OAuth'])


class UserAuthorizeResultData(BaseModel):
    client_id: str
    redirect_uri: HttpUrl
    scope: str
    allow: bool


@router.get('/authorize')
async def user_authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str
):
    # return RedirectResponse(url=f'/#/?authorize=oauth&response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}')
    return JSONResponse(content={
        'response_type': response_type,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope
    })


@router.post('/authorize')
async def user_authorize_result(
    payload: UserAuthorizeResultData,
    user_session_info: UserSession = Depends(get_current_user_session),
    db: AsyncSession = Depends(get_db)
):
    # TODO: add logs
    if not payload.allow:
        return BaseApiResp(status='error', msg='UserDenied')
    expires_at = datetime.now(UTC) + timedelta(minutes=5)

    new_auth_code = OAuthAuthorizationCode(
        client_id=payload.client_id,
        redirect_uri=payload.redirect_uri,
        scope=payload.scope,
        user=user_session_info.user,
        expires_at=expires_at
    )
    db.add(new_auth_code)
    await db.commit()
    await db.refresh(new_auth_code)
    return BaseApiResp(
        status='OK',
        msg='AllDone',
        payload={'code': new_auth_code.code}
    )


@router.post('/token')
async def token():
    return
