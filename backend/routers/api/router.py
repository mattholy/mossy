# -*- encoding: utf-8 -*-
'''
router.py
----
定义各种路由


@Time    :   2024/04/12 16:44:04
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter
from routers.api.m1 import router as api_m1_router
from routers.api.v1 import router as api_v1_router
from routers.api.v2 import router as api_v2_router

from env import API_BASE_URL

router = APIRouter(prefix=API_BASE_URL, tags=['API'])

router.include_router(api_m1_router)
router.include_router(api_v1_router)
router.include_router(api_v2_router)
