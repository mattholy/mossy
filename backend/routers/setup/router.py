# -*- encoding: utf-8 -*-
'''
router.py
----
Mossy setup api


@Time    :   2024/04/30 22:57:57
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, Field
from typing import Optional

from utils.model.api_schemas import ApiServiceSetupStatus, BaseApiResp, WebauthnReg
from utils.db import get_db
from utils.model.orm import SystemConfig
from utils.init import init_node, ready
from routers.api.m1.authentication.endpoint import start_registration

router = APIRouter(prefix='/setup', tags=['Mossy Setup'])


@router.post('/status', response_model=ApiServiceSetupStatus)
async def setup_status(db: AsyncSession = Depends(get_db)):
    return ApiServiceSetupStatus(status='OK', msg='AllDone', payload={'status': ready(return_stage=True)})


class ServerBanner(BaseModel):
    file_name: str = ''
    file_count: int = 0
    file_size: int = 0
    file_type: str = ''
    file_content: str = ''
    isTwoToOne: bool = False


class SetupForm(BaseModel):
    server_name: str = ''
    server_desc: str = ''
    server_admin: str = ''
    server_service: str = ''
    server_about: str = ''
    server_banner: ServerBanner = Field(default_factory=ServerBanner)
    server_status: str = ''
    server_isolated: bool = False
    server_telemetry: bool = True
    server_union: bool = True


@router.post('/init', response_model=BaseApiResp)
async def setup_status(basic_info: SetupForm, db: AsyncSession = Depends(get_db)):
    if ready():
        raise HTTPException(status_code=403, detail='AlreadyInit')
    try:
        for key in basic_info.model_fields.keys():
            if key == 'server_banner':
                db.add(SystemConfig(key='server_banner',
                       value=basic_info.server_banner.file_content))
                continue
            db.add(SystemConfig(key=key, value=str(getattr(basic_info, key))))
        db.add(SystemConfig(key='init_flag', value='AllDone'))
        await db.commit()
    except Exception as e:
        raise e
    return BaseApiResp(status='OK', msg='AllDone', payload={})
