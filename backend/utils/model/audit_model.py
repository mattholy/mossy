# -*- encoding: utf-8 -*-
'''
audit_model.py
----
put some words here


@Time    :   2024/05/19 13:05:52
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

# here put the import lib
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class AuthModule(BaseModel):
    user: str = Field(example='admin')
    operation: Literal['login', 'register'] = Field(example='login')
