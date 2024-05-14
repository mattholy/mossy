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
from env import RP_ID
from utils.model.orm import SystemConfig
from utils.db import get_db
from utils.tools import get_value_or_default

router = APIRouter(prefix='/instance',
                   tags=['API', 'v1', 'Mastodon-Compatible'])


# @router.get(
#     '',
#     deprecated=True,
#     response_class=JSONResponse,
#     response_model=InstanceV1
# )
# async def fetch_instance(db: AsyncSession = Depends(get_db)):
#     '''
#     Fetch instance information
#     '''
#     keys_to_fetch = [
#         'server_name',
#         'server_desc'
#     ]
#     query = select(SystemConfig).filter(SystemConfig.key.in_(keys_to_fetch))
#     results = await db.execute(query)
#     config_dict = {result.key: result.value for result in results.scalars()}

#     instance = InstanceV1(
#         uri=RP_ID,
#         title=get_value_or_default(config_dict.get(
#             'server_name'), 'Default Server Name'),
#         short_description=get_value_or_default(
#             config_dict.get('server_name'), 'Default Server Name')
#     )
#     return instance
