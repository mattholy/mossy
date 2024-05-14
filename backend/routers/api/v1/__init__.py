# -*- encoding: utf-8 -*-
'''
__init__.py
----
ActivityPub API v1


@Time    :   2024/05/07 13:24:17
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter
from routers.api.v1.instance.endpoint import router as instance_router
from routers.api.v1.apps.endpoint import router as apps_router

router = APIRouter(prefix='/v1', tags=['API', 'v1'])
router.include_router(instance_router)
router.include_router(apps_router)
