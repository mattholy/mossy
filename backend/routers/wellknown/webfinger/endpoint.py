# -*- encoding: utf-8 -*-
'''
endpoint.py
----
webfinger endpoints


@Time    :   2024/04/30 13:41:24
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter

router = APIRouter(prefix='/webfinger', tags=['Webfinger'])


@router.get('/')
def webfinger(resource: str):
    print(resource)
    assert resource.startswith('acct:'), 'Invalid resource'
    return 'webfinger'
