# -*- encoding: utf-8 -*-
'''
__init__.py
----
Public asset router


@Time    :   2024/05/21 16:08:53
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import uuid
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix='/asset', tags=['Assets'])


@router.get('/{res_id: uuid.UUID}', response_class=FileResponse)
async def fetch_public_asset(res_id: uuid.UUID):
    pass
