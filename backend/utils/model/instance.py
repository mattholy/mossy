# -*- encoding: utf-8 -*-
'''
instance.py
----
used for instance model by mastodon and others


@Time    :   2024/05/10 14:37:11
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from pydantic import BaseModel, AnyUrl, HttpUrl
from typing import List, Optional, Dict, Union, Any

# Common models used in both V1 and V2


class StreamingAPI(BaseModel):
    streaming_api: AnyUrl


class Stats(BaseModel):
    user_count: int
    status_count: int
    domain_count: int


class MediaAttachmentsConfig(BaseModel):
    supported_mime_types: List[str]
    image_size_limit: int
    image_matrix_limit: int
    video_size_limit: int
    video_frame_rate_limit: int
    video_matrix_limit: int


class StatusesConfig(BaseModel):
    max_characters: int
    max_media_attachments: int
    characters_reserved_per_url: int


class PollsConfig(BaseModel):
    max_options: int
    max_characters_per_option: int
    min_expiration: int
    max_expiration: int


class Configuration(BaseModel):
    statuses: StatusesConfig
    media_attachments: MediaAttachmentsConfig
    polls: PollsConfig


class Rule(BaseModel):
    id: str
    text: str


class ThumbnailV1(BaseModel):
    url: Optional[HttpUrl]


class ThumbnailV2(BaseModel):
    url: HttpUrl
    blurhash: Optional[str]
    versions: Dict[str, HttpUrl]


class Registration(BaseModel):
    enabled: bool
    approval_required: bool
    message: Optional[str]


class Usage(BaseModel):
    users: Dict[str, int]


class Role(BaseModel):
    id: str
    name: str
    color: str


class Field(BaseModel):
    name: str
    value: str
    verified_at: Optional[Any]  # 使用 Any 是因为你的示例中这个字段为 null


class Account(BaseModel):
    id: str
    username: str
    acct: str
    display_name: str
    locked: bool
    bot: bool
    discoverable: bool
    group: bool
    created_at: str
    note: str
    url: Optional[HttpUrl]
    uri: Optional[HttpUrl]
    avatar: HttpUrl
    avatar_static: HttpUrl
    header: HttpUrl
    header_static: HttpUrl
    followers_count: int
    following_count: int
    statuses_count: int
    last_status_at: str
    noindex: bool
    emojis: List[str]
    roles: Optional[List[Role]]
    fields: List[Field]


class Contact(BaseModel):
    email: Optional[str]
    account: Account

# Version specific models


class InstanceV1(BaseModel):
    uri: str
    title: str
    short_description: str
    description: str
    email: str
    version: str
    urls: StreamingAPI
    stats: Stats
    thumbnail: Optional[ThumbnailV1]
    languages: List[str]
    registrations: bool
    approval_required: bool
    invites_enabled: bool
    configuration: Configuration
    contact_account: Optional[str]  # Simplified for demonstration
    rules: List[Rule]


class InstanceV2(BaseModel):
    domain: str
    title: str
    version: str
    source_url: HttpUrl
    description: str
    usage: Usage
    thumbnail: ThumbnailV2
    languages: List[str]
    configuration: Configuration
    registrations: Registration
    contact: Contact
    rules: List[Rule]
