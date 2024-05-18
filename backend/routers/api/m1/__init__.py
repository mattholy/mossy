# -*- encoding: utf-8 -*-
'''
__init__.py
----
Mossy's api mark 1


@Time    :   2024/05/07 13:21:20
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter
from routers.api.m1.authentication.endpoint import router as authentication_router
from routers.api.m1.server.endpoint import router as server_router

router = APIRouter(prefix='/m1', tags=['API', 'm1'])
router.include_router(authentication_router)
router.include_router(server_router)
