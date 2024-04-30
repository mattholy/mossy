# -*- encoding: utf-8 -*-
'''
router.py
----
.well-known endpoints


@Time    :   2024/04/30 13:42:33
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from routers.wellknown.webfinger.endpoint import router as webfinger_router
from routers.wellknown.nodeinfo.endpoint import router as nodeinfo_router
from fastapi import APIRouter

router = APIRouter(prefix='/.well-known', tags=['Well-known'])

router.include_router(webfinger_router)
router.include_router(nodeinfo_router)
