# -*- encoding: utf-8 -*-
'''
nodeinfo.py
----
schema for nodeinfo


@Time    :   2024/04/30 14:29:50
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# Nodeinfo 2.0 schema


class Software2dot0(BaseModel):
    name: str = Field(..., pattern=r'^[a-z0-9-]+$')
    version: str


class ServiceLists2dot0(BaseModel):
    inbound: List[str] = Field(
        default_factory=list, description="Sites for inbound service connections")
    outbound: List[str] = Field(
        default_factory=list, description="Sites for outbound service connections")


class UserStats2dot0(BaseModel):
    total: int = Field(..., ge=0)
    activeHalfyear: int = Field(..., ge=0)
    activeMonth: int = Field(..., ge=0)


class UsageStats2dot0(BaseModel):
    users: UserStats2dot0
    local_posts: int = Field(..., ge=0, alias='localPosts')
    local_comments: int = Field(..., ge=0, alias='localComments')


class NodeInfo2dot0(BaseModel):
    version: str = '2.0'
    software: Software2dot0
    protocols: List[str]
    services: ServiceLists2dot0
    openRegistrations: bool = Field(alias="open_registrations")
    usage: UsageStats2dot0
    metadata: dict

    class Config:
        populate_by_name = True

# Nodeinfo 2.1 schema


class Software2dot1(BaseModel):
    name: str = Field(pattern=r'^[a-z0-9-]+$')
    version: str
    repository: str = Field(...,
                            description="URL of the source code repository")
    homepage: str = Field(..., description="URL of the homepage")


class ServiceLists2dot1(BaseModel):
    inbound: List[str] = Field(
        default_factory=list, description="Sites for inbound service connections")
    outbound: List[str] = Field(
        default_factory=list, description="Sites for outbound service connections")


class UserStats2dot1(BaseModel):
    total: int = Field(..., ge=0)
    activeHalfyear: int = Field(..., ge=0)
    activeMonth: int = Field(..., ge=0)


class UsageStats2dot1(BaseModel):
    users: UserStats2dot1
    localPosts: int = Field(..., ge=0)
    localComments: int = Field(..., ge=0)


class NodeInfo2dot1(BaseModel):
    version: str = '2.1'
    software: Software2dot1
    protocols: List[str]
    services: ServiceLists2dot1
    openRegistrations: bool = Field(..., alias="open_registrations")
    usage: UsageStats2dot1
    metadata: Dict[str, Optional[str]] = Field(default_factory=dict)

    class Config:
        populate_by_name = True
