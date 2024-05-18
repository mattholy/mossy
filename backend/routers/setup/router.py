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

import base64
from PIL import Image, UnidentifiedImageError
import io
import re
from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi import status as resp_status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, Field
from typing import Optional

from utils.model.api_schemas import ApiServiceSetupStatus, BaseApiResp, WebauthnReg
from utils.db import get_db
from utils.model.orm import SystemConfig
from utils.init import init_node, ready
from utils.logger import logger, async_log_error_to_db
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
    server_name: str
    server_desc: str = ''
    server_admin: str
    server_service: str = ''
    server_about: str = ''
    server_banner: ServerBanner = Field(default_factory=ServerBanner)
    server_status: str = ''
    server_isolated: bool = False
    server_telemetry: bool = True
    server_allow_search: bool = True
    server_union: bool = True


@router.post('/init', response_model=BaseApiResp)
async def setup_status(basic_info: SetupForm, request: Request, db: AsyncSession = Depends(get_db)):
    if ready():
        raise HTTPException(status_code=403, detail='AlreadyInit')
    try:
        # check banner image
        if basic_info.server_banner.file_size > 0:
            try:
                img_base64 = basic_info.server_banner.file_content
                if img_base64.startswith('data:'):
                    if not img_base64.startswith('data:image'):
                        raise UnidentifiedImageError
                    img_base64 = img_base64.split(',')[1]
                image_data = base64.b64decode(img_base64)
                image = Image.open(io.BytesIO(image_data))
                width, height = image.size
                aspect_ratio = width / height
                tolerance = 0.05
                is_close_to_two_to_one = (
                    2 - tolerance) <= aspect_ratio <= (2 + tolerance)
                if is_close_to_two_to_one != basic_info.server_banner.isTwoToOne:
                    raise HTTPException(
                        status_code=400, detail='BannerImageAspectError')
            except UnidentifiedImageError as e:
                raise HTTPException(
                    status_code=400, detail='BannerImageFormatError')
            except Exception as e:
                await async_log_error_to_db(
                    e, request.app.state.node_id, request.app.state.worker_id)
                raise HTTPException(status_code=400, detail='UnknownError')
        # check server admin name
        pattern = re.compile(r'^[a-zA-Z0-9_-]{3,32}$')
        if not pattern.match(basic_info.server_admin):
            raise HTTPException(status_code=400, detail='AdminNameError')
        for key in basic_info.model_fields.keys():
            if key == 'server_banner':
                db.add(SystemConfig(key='server_banner',
                       value=basic_info.server_banner.file_content))
                db.add(SystemConfig(key='server_banner_mime',
                       value=basic_info.server_banner.file_type))
                continue
            db.add(SystemConfig(key=key, value=str(getattr(basic_info, key))))
        db.add(SystemConfig(key='init_flag', value='AllDone'))
        await db.commit()
    except Exception as e:
        raise e
    return BaseApiResp(status='OK', msg='AllDone', payload={})
