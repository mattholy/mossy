# -*- encoding: utf-8 -*-
"""
endpoint.py
----
put some words here


@Time    :   2024/05/19 23:23:46
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
"""

import json
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field, AnyUrl, validator
from typing import List, Optional
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    options_to_json,
    base64url_to_bytes,
    generate_authentication_options,
    verify_authentication_response,
)

from sqlalchemy import func
from webauthn.helpers.exceptions import (
    InvalidRegistrationResponse,
    InvalidAuthenticationResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from webauthn.helpers.structs import PublicKeyCredentialCreationOptions

from utils.db import get_db
from utils.model.api_schemas import BaseApiResp
from utils.model.orm import (
    Passkeys,
    AuthSession,
    SystemConfig,
    ServerRules,
    MossyUser,
    FediAccounts,
)
from utils.system.security import (
    generate_jwt,
    verify_jwt,
    get_current_user_session,
    generate_ecc_key_pair,
)
from utils.system.security import UserSession
from utils.logger import logger

from env import RP_ID, RP_NAME, RP_SOURCE, DATABASE_URL

router = APIRouter(prefix="/user", tags=["User Related"])


class Avatar(BaseModel):
    file_content: Optional[str] = Field(
        "", description="Base64 encoded content of the avatar file"
    )
    file_type: Optional[str] = Field("", description="MIME type of the avatar file")
    file_size: int = Field(0, description="Size of the avatar file in bytes")

    @validator("file_content", "file_type", pre=True, always=True)
    def set_empty_string_if_none(cls, v):
        return v or ""

    @validator("file_size", pre=True, always=True)
    def set_zero_if_none(cls, v):
        return v or 0


class Header(BaseModel):
    file_content: Optional[str] = Field(
        "", description="Base64 encoded content of the header file"
    )
    file_type: Optional[str] = Field("", description="MIME type of the header file")
    file_size: int = Field(0, description="Size of the header file in bytes")

    @validator("file_content", "file_type", pre=True, always=True)
    def set_empty_string_if_none(cls, v):
        return v or ""

    @validator("file_size", pre=True, always=True)
    def set_zero_if_none(cls, v):
        return v or 0


class UserProfile(BaseModel):
    uid: str = Field()
    display_name: str = Field("John Doe", description="Display name of the user")
    desc: str = Field("", description="Description of the user")
    avatar: Avatar = Field(default_factory=Avatar, description="Avatar of the user")
    header: Header = Field(default_factory=Header, description="Header of the user")
    fields: List[Optional[dict]] = Field(
        default_factory=list, description="List of additional fields"
    )

    @validator("desc", pre=True, always=True)
    def set_empty_string_if_none(cls, v):
        return v or ""

    @validator("fields", pre=True, always=True)
    def set_empty_list_if_none(cls, v):
        return v or []


class UserProfilesResp(BaseApiResp):
    status: str = "OK"
    msg: str = "AllDone"
    payload: UserProfile


@router.get("/profile", response_model=UserProfilesResp)
async def fetch_user_profile(
    user_session: UserSession = Depends(get_current_user_session),
    db: AsyncSession = Depends(get_db),
):
    fedi_user_query = (
        select(FediAccounts)
        .where(
            FediAccounts.username == user_session.user and FediAccounts.domain == RP_ID
        )
        .limit(1)
    )
    fedi_user_res = await db.execute(fedi_user_query)
    fedi_user = fedi_user_res.scalars().first()
    if fedi_user is not None:
        user_profile = UserProfile(
            uid=fedi_user.username,
            display_name=fedi_user.display_name,
            desc=fedi_user.description_in_markdown,
            avatar=Avatar(
                file_content=fedi_user.avatar_file_content,
                file_size=fedi_user.avatar_file_size,
                file_type=fedi_user.avatar_file_type,
            ),
            header=Header(
                file_content=fedi_user.header_file_content,
                file_size=fedi_user.header_file_size,
                file_type=fedi_user.header_file_type,
            ),
            fields=fedi_user.fields,
        )
    else:
        user_profile = UserProfile(
            display_name="",
            desc="",
            avatar=Avatar(file_content="", file_size=0, file_type=""),
            header=Header(file_content="", file_size=0, file_type=""),
            fields=[],
        )
    return UserProfilesResp(payload=user_profile)


@router.post("/profile", response_model=UserProfilesResp)
async def fetch_user_profile(
    profile_data: UserProfile,
    user_session: UserSession = Depends(get_current_user_session),
    db: AsyncSession = Depends(get_db),
):
    logger.debug(profile_data.avatar.file_type)
    fedi_user_query = (
        select(FediAccounts)
        .where(
            FediAccounts.username == user_session.user and FediAccounts.domain == RP_ID
        )
        .limit(1)
    )
    fedi_user_res = await db.execute(fedi_user_query)
    fedi_user = fedi_user_res.scalars().first()
    if fedi_user is None:
        raise HTTPException(status_code=401, detail="UserNotFound")
    fedi_user.display_name = profile_data.display_name
    fedi_user.description_in_markdown = profile_data.desc  # TODO: update this to html
    fedi_user.avatar_file_content = profile_data.avatar.file_content
    fedi_user.avatar_file_size = profile_data.avatar.file_size
    fedi_user.avatar_file_type = profile_data.avatar.file_type
    fedi_user.header_file_content = profile_data.header.file_content
    fedi_user.header_file_size = profile_data.header.file_size
    fedi_user.header_file_type = profile_data.header.file_type
    fedi_user.fields = profile_data.fields
    user_profile = UserProfile(
        uid=fedi_user.username,
        display_name=fedi_user.display_name,
        desc=fedi_user.description_in_markdown,
        avatar=Avatar(
            file_content=fedi_user.avatar_file_content,
            file_size=fedi_user.avatar_file_size,
            file_type=fedi_user.avatar_file_type,
        ),
        header=Header(
            file_content=fedi_user.header_file_content,
            file_size=fedi_user.header_file_size,
            file_type=fedi_user.header_file_type,
        ),
        fields=fedi_user.fields,
    )
    await db.commit()
    return UserProfilesResp(payload=user_profile)


@router.get("/asset/{res_id: uuid.UUID}", tags=["Assets"])
async def fetch_user_asset(
    res_id: uuid.UUID,
    user_session: UserSession = Depends(get_current_user_session),
    db: AsyncSession = Depends(get_db),
):
    """Get the asset of the user"""
    pass


@router.get("/asset", tags=["Assets"])
async def fetch_user_asset(
    res_id: uuid.UUID,
    user_session: UserSession = Depends(get_current_user_session),
    db: AsyncSession = Depends(get_db),
):
    """Get the assets list of the user"""
    pass


@router.post("/asset/{res_id: uuid.UUID}", tags=["Assets"])
async def update_user_asset(
    res_id: uuid.UUID,
    user_session: UserSession = Depends(get_current_user_session),
    db: AsyncSession = Depends(get_db),
):
    """Post any binary here to update the asset, post nothing to delete the asset"""
    pass


@router.post("/asset", tags=["Assets"])
async def upload_user_asset(
    user_session: UserSession = Depends(get_current_user_session),
    db: AsyncSession = Depends(get_db),
):
    """Post any binary here to upload user asset"""
    pass
