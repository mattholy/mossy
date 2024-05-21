# -*- encoding: utf-8 -*-
'''
router.py
----
put some words here


@Time    :   2024/05/21 16:06:41
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter
from routers.public.asset import router as asset_router

from env import PUBLIC_BASE_URL

router = APIRouter(prefix=PUBLIC_BASE_URL, tags=['Public Access'])

router.include_router(asset_router)
