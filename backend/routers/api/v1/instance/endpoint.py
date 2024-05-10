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
from fastapi.responses import JSONResponse

from utils.model.instance import InstanceV1

router = APIRouter(prefix='/instance', tags=['API', 'v1'])


@router.get('', deprecated=True, response_class=JSONResponse, response_model=InstanceV1)
def fetch_instance():
    return None
