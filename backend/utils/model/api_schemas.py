# -*- encoding: utf-8 -*-
'''
api.py
----
接口数据模型


@Time    :   2024/04/12 16:59:48
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''
from typing import Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: str
    msg: str


class WebauthnReg(BaseResponse):
    payload: Optional[dict]


class BaseApiResp(BaseResponse):
    payload: Optional[dict]


class ServiceSetupStatus(BaseModel):
    status: str


class ApiServiceSetupStatus(BaseApiResp):
    payload: ServiceSetupStatus
