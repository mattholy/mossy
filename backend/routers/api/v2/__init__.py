# -*- encoding: utf-8 -*-
'''
__init__.py
----
ActivityPub API v2


@Time    :   2024/05/07 13:17:56
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter

router = APIRouter(prefix='/v2', tags=['API', 'v2'])
