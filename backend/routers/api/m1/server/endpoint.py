# -*- encoding: utf-8 -*-
'''
endpoint.py
----
put some words here


@Time    :   2024/05/18 15:37:03
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import json
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field, AnyUrl
from typing import List, Optional
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    options_to_json,
    base64url_to_bytes,
    generate_authentication_options,
    verify_authentication_response
)

from sqlalchemy import func
from webauthn.helpers.exceptions import InvalidRegistrationResponse, InvalidAuthenticationResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from webauthn.helpers.structs import PublicKeyCredentialCreationOptions

from utils.db import get_db
from utils.model.api_schemas import BaseApiResp
from utils.model.orm import Passkeys, AuthSession, SystemConfig, ServerRules, MossyUser, FediAccounts
from utils.system.security import generate_jwt, verify_jwt, get_current_user_session
from utils.logger import logger

from env import RP_ID, RP_NAME, RP_SOURCE, DATABASE_URL

router = APIRouter(prefix='/server', tags=['Server Configuration'])


class ServerRule(BaseModel):
    order: int = Field(example=1)
    content: str = Field(example='Rule 1')
    updated_at: datetime = Field(example=datetime.now(timezone.utc))


class ServerInfo(BaseModel):
    title: str = Field(example='Mossy')
    admin_id: str = Field(example='admin')
    admin_name: str = Field(example='Administrator')
    admin_avatar: str = Field(example='data:image/png;base64,xxx')
    server_banner: str = Field(example='data:image/png;base64,xxx')
    contact: AnyUrl | str = Field(example='mailto:admin@localhost')
    users: int = Field(example=999)
    users_of_30: int = Field(example=999)
    description: str = Field(
        example='Mossy is a simple and easy-to-use forum software.')
    about: str = Field(example='# Mossy')
    rules: List[ServerRule] = Field(
        example=[{'order': 1, 'content': 'Rule 1'}])


class ServerInfoResp(BaseApiResp):
    payload: ServerInfo


@router.get('/info', response_class=JSONResponse, response_model=ServerInfoResp)
async def fetch_server_info(db: AsyncSession = Depends(get_db)):
    keys_to_fetch = [
        'server_name',
        'server_desc',
        'server_banner',
        'server_banner_mime',
        'server_service',
        'server_admin',
        'server_about',
        'server_desc'
    ]
    query = select(SystemConfig).filter(SystemConfig.key.in_(keys_to_fetch))
    results = await db.execute(query)
    config_dict = {result.key: result.value for result in results.scalars()}

    rules_query = select(ServerRules).order_by(ServerRules.id)
    rules_query_results = await db.execute(rules_query)
    rules = rules_query_results.scalars().all()
    rules_list = [{'order': rule.id, 'content': rule.content, 'updated_at': rule.updated_at}
                  for rule in rules]
    logger.debug(rules_list)

    users_count_query = select(func.count(func.distinct(MossyUser.id))).where(
        MossyUser.id > 0)
    users_count_result = await db.execute(users_count_query)
    unique_user_count = users_count_result.scalar()
    logger.debug(unique_user_count)

    thirty_days_ago = datetime.now() - timedelta(days=30)
    users_of_30_query = select(func.count(func.distinct(AuthSession.user))).where(
        AuthSession.created_at >= thirty_days_ago)
    users_of_30_result = await db.execute(users_of_30_query)
    users_of_30_count = users_of_30_result.scalar()

    admin_query = select(FediAccounts).where(
        FediAccounts.username == config_dict['server_admin'])
    admin_result = await db.execute(admin_query)
    admin = admin_result.scalars().first()

    return ServerInfoResp(
        payload=ServerInfo(
            title=config_dict['server_name'],
            admin_id=config_dict['server_admin'],
            admin_name=admin.display_name if admin else '',
            admin_avatar=f'data:{admin.avatar_file_type};base64,{
                admin.avatar_file_content}' if admin else '',
            server_banner=f'data:{config_dict["server_banner_mime"]};base64,{
                config_dict["server_banner"]}' if config_dict["server_banner"] else '',
            contact=config_dict['server_service'],
            users=unique_user_count,
            users_of_30=users_of_30_count,
            description=config_dict['server_desc'],
            about=config_dict['server_about'],
            rules=rules_list
        ),
        status='OK',
        msg='AllDone'
    )
