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
from pydantic import BaseModel

from utils.model.api_schemas import BaseResponse
from utils.db import get_db
from utils.model.orm import SystemConfig

router = APIRouter(prefix='/setup', tags=['Mossy Setup'])


@router.post('/status', response_model=BaseResponse)
async def setup_status(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SystemConfig).filter_by(key='init_flag'))
    init_flag = result.scalars().first()
    # if init
    if init_flag and init_flag.value == 'All-Done':
        raise HTTPException(status_code=403, detail='AlreadyInit')
    # if not init
    return BaseResponse(status='OK', msg='AllDone')


class BasicInfo(BaseModel):
    planet_name: str
    planet_desc: str
    planet_owner_username: str
    offline_mode: bool
    mossy_network: bool


@router.post('/init', response_model=BaseResponse)
async def setup_status(basic_info: BasicInfo, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SystemConfig).filter_by(key='init_flag'))
    init_flag = result.scalars().first()
    # if init
    if init_flag and init_flag.value == 'All-Done':
        raise HTTPException(status_code=403, detail='AlreadyInit')
    try:
        conf_planet_name = SystemConfig(
            key='planet_name',
            value=basic_info.planet_name
        )
        conf_planet_desc = SystemConfig(
            key='planet_desc',
            value=basic_info.planet_desc
        )
        conf_planet_owner = SystemConfig(
            key='planet_owner_username',
            value=basic_info.planet_owner_username
        )
        conf_offline_mode = SystemConfig(
            key='offline_mode',
            value='OFFLINE' if basic_info.offline_mode else 'ONLINE'
        )
        conf_mossy_network = SystemConfig(
            key='mossy_network',
            value='ENABLE' if basic_info.mossy_network else 'DISABLE'
        )
        conf_finished = SystemConfig(
            key='init_flag',
            value='All-Done'
        )
        db.add_all([
            conf_planet_name,
            conf_planet_desc,
            conf_planet_owner,
            conf_offline_mode,
            conf_mossy_network,
            conf_finished
        ])
        await db.commit()
        return BaseResponse(status='OK', msg='AllDone')
    except Exception as e:
        raise e
