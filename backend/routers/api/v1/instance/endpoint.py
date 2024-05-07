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

from fastapi import APIRouter

router = APIRouter(prefix='/instance', tags=['API', 'v1'])


@router.get('')
def fetch_instance():
    return {}
