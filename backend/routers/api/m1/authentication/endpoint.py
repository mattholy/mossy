# -*- encoding: utf-8 -*-
"""
auth.py
----
登陆和认证


@Time    :   2024/04/12 16:49:39
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
"""

import json
import jwt
import uuid
import hashlib
import random
import string
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    options_to_json,
    base64url_to_bytes,
    generate_authentication_options,
    verify_authentication_response,
)

from webauthn.helpers.exceptions import (
    InvalidRegistrationResponse,
    InvalidAuthenticationResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from webauthn.helpers.structs import (
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialRequestOptions,
)

from utils.db import get_db
from utils.model.api_schemas import WebauthnReg
from utils.model.orm import (
    generate_secret,
    Passkeys,
    AuthChallenges,
    AuthSession,
    MossyUser,
    FediAccounts,
)
from utils.system.security import (
    generate_jwt,
    verify_jwt,
    get_current_user_session,
    generate_ecc_key_pair,
)
from utils.logger import logger, async_operation_log_to_db

from env import RP_ID, RP_NAME, RP_SOURCE, DATABASE_URL


router = APIRouter(prefix="/auth", tags=["Authentication"])


class User(BaseModel):
    username: str = Field(pattern=r"^[a-zA-Z0-9_-]+$", min_length=3, max_length=64)


@router.post(
    "/generate-registration-options",
    response_class=JSONResponse,
    response_model=WebauthnReg,
)
async def start_registration(
    user: User, request: Request, db: AsyncSession = Depends(get_db)
):
    user_agent = request.headers.get("user-agent", "unknown")
    access_address = request.client.host
    # Check if there is a registration process of the user
    result = await db.execute(select(AuthChallenges).filter_by(user=user.username))
    go_find_user = result.scalars().first()
    # Check if user already exists
    if_exists = await db.execute(select(Passkeys).filter_by(user=user.username))
    user_exists = if_exists.scalars().first()

    if user_exists or (
        go_find_user
        and go_find_user.created_at > datetime.now(timezone.utc) - timedelta(minutes=3)
    ):
        raise HTTPException(status_code=403, detail="UserAlreadyExist")

    if go_find_user and go_find_user.created_at < datetime.now(
        timezone.utc
    ) - timedelta(minutes=3):
        logger.debug(
            f"User {user.username} registration process timeout, deleting the process. Registered at {go_find_user.created_at}, now {datetime.now(timezone.utc)}"
        )
        await db.delete(go_find_user)

    simple_registration_options: PublicKeyCredentialCreationOptions = (
        generate_registration_options(
            rp_id=RP_ID,
            rp_name=RP_NAME,
            user_name=user.username,
            user_display_name=user.username,
            user_id=user.username.encode("utf-8"),
        )
    )

    new_challenge = AuthChallenges(
        challenge=simple_registration_options.challenge,
        user_agent=user_agent,
        access_address=access_address,
        user=user.username,
    )
    db.add(new_challenge)
    await db.commit()
    await db.refresh(new_challenge)
    return WebauthnReg(
        status="OK",
        msg="AllDone",
        payload={
            "mossy_id": new_challenge.uuid,
            "webauthn": json.loads(options_to_json(simple_registration_options)),
        },
    )


@router.post(
    "/verify-registration", response_class=JSONResponse, response_model=WebauthnReg
)
async def after_registration(
    request_data: dict, request: Request, db: AsyncSession = Depends(get_db)
):
    user_agent = request.headers.get("user-agent", "unknown")
    access_address = request.client.host

    result = await db.execute(
        select(AuthChallenges).filter_by(uuid=request_data["mossy_id"])
    )
    att = result.scalars().first()
    if not att:
        raise HTTPException(status_code=401, detail="NoChallenge")
    if not att.user:
        raise HTTPException(status_code=401, detail="NoUser")
    user_request = att.user

    if att.created_at < datetime.now(timezone.utc) - timedelta(minutes=3):
        await db.delete(att)
        await db.commit()
        raise HTTPException(status_code=406, detail="RegistrationTimeOut")

    mossy_user_query = await db.execute(select(MossyUser).filter_by(username=att.user))
    mossy_user = mossy_user_query.scalars().first()
    try:
        registration_verification = verify_registration_response(
            credential=request_data["payload"],
            expected_challenge=att.challenge,
            expected_origin=RP_SOURCE,
            expected_rp_id=RP_ID,
            require_user_verification=True,
        )
        new_key = Passkeys(
            user=user_request,
            credential_id=registration_verification.credential_id,
            public_key=registration_verification.credential_public_key,
            device_type=registration_verification.credential_device_type.name,
            annotate="Passkey@" + att.access_address,
            transports=",".join(request_data["payload"]["response"]["transports"]),
            sign_count=registration_verification.sign_count,
            registered_user_agent=att.user_agent,
            raw_id=request_data["payload"]["rawId"],
        )
        # register user if not exists (for the first time registration)
        if not mossy_user:
            r_key = "-".join(
                ["".join(random.choices(string.ascii_lowercase, k=6)) for _ in range(4)]
            )
            ag = hashlib.sha256()
            ag.update((r_key + "@" + user_request).encode("utf-8"))
            mossy_user = MossyUser(
                username=user_request,
                registration_source=request_data["register_from"],
                recovery_key=ag.hexdigest(),
            )
            db.add(mossy_user)
        db.add(new_key)
        db.delete(att)
        await db.commit()
        await async_operation_log_to_db(
            "auth",
            {
                "operation": "register",
                "user": user_request,
            },
        )
        if r_key:
            return WebauthnReg(
                status="OK", msg="AllDone", payload={"recovery_key": r_key}
            )
        return WebauthnReg(status="OK", msg="AllDone", payload=None)
    except InvalidRegistrationResponse as e:
        if str(e).startswith("Unexpected client data origin"):
            raise HTTPException(status_code=401, detail="InvalidOrigin")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise e


@router.post(
    "/generate-authentication-options",
    response_class=JSONResponse,
    response_model=WebauthnReg,
)
async def start_authentication(request: Request, db: AsyncSession = Depends(get_db)):
    user_agent = request.headers.get("user-agent", "unknown")
    access_address = request.client.host
    simple_authentication_options: PublicKeyCredentialRequestOptions = (
        generate_authentication_options(
            rp_id=RP_ID,
        )
    )
    new_challenge = AuthChallenges(
        challenge=simple_authentication_options.challenge,
        user_agent=user_agent,
        access_address=access_address,
    )
    db.add(new_challenge)
    await db.commit()
    await db.refresh(new_challenge)
    return WebauthnReg(
        status="OK",
        msg="AllDone",
        payload={
            "mossy_id": new_challenge.uuid,
            "webauthn": json.loads(options_to_json(simple_authentication_options)),
        },
    )


@router.post(
    "/verify-authentication", response_class=JSONResponse, response_model=WebauthnReg
)
async def after_authentication(
    req_data: dict, request: Request, db: AsyncSession = Depends(get_db)
):
    passkey_result = await db.execute(
        select(Passkeys).filter_by(raw_id=req_data["payload"]["rawId"])
    )
    passkey = passkey_result.scalars().first()
    if passkey is None:
        raise HTTPException(status_code=401, detail="NoPublicKey")
    challenge_result = await db.execute(
        select(AuthChallenges).filter_by(uuid=req_data["mossy_id"])
    )
    challenge = challenge_result.scalars().first()
    if challenge is None:
        raise HTTPException(status_code=401, detail="NoChallenge")
    try:
        authentication_verification = verify_authentication_response(
            credential=req_data["payload"],
            expected_challenge=challenge.challenge,
            expected_rp_id=RP_ID,
            expected_origin=RP_SOURCE,
            credential_public_key=passkey.public_key,
            credential_current_sign_count=passkey.sign_count,
            require_user_verification=True,
        )
        passkey.sign_count = authentication_verification.new_sign_count
        token, payload = generate_jwt(passkey.user_secret, passkey.user)
        new_session = AuthSession(
            id=payload["jti"],
            user=passkey.user,
            source="LOGIN_SESSION",
            expiry_date=payload["exp"],
            is_active=True,
            user_agent=request.headers.get("user-agent", "unknown"),
            related_passkey=passkey.id,
        )
        db.add(new_session)
        # check if need to setup profile
        fedi_acc_result = await db.execute(
            select(FediAccounts).filter_by(username=passkey.user).limit(1)
        )
        fedi_acc_result = fedi_acc_result.scalars().first()
        green = False
        if not fedi_acc_result:
            private_key_pem, public_key_pem = generate_ecc_key_pair()
            fedi_acc_result = FediAccounts(
                username=passkey.user,
                public_key=public_key_pem,
                private_key=private_key_pem,
                display_name="Mossy Momo",
                description_in_markdown="A New Mossy Momo User",
            )
            green = True
            db.add(fedi_acc_result)
        await db.commit()
        return WebauthnReg(
            status="OK", msg="AllDone", payload={"token": token, "green": green}
        )
    except InvalidAuthenticationResponse as e:
        if str(e).startswith("Unexpected client data origin"):
            raise HTTPException(status_code=401, detail="InvalidOrigin")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise e


class AuthJWT(BaseModel):
    token: str


@router.post("/verify-jwt", response_class=JSONResponse, response_model=WebauthnReg)
async def check_jwt(
    auth_jwt: AuthJWT, request: Request, db: AsyncSession = Depends(get_db)
):
    res = await verify_jwt(
        auth_jwt.token, request.headers.get("user-agent", "unknown"), db=db
    )
    if res:
        return WebauthnReg(status="OK", msg="AllDone", payload=None)
    else:
        raise HTTPException(status_code=401, detail="InvalidToken")
