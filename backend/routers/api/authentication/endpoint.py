# -*- encoding: utf-8 -*-
'''
auth.py
----
登陆和认证


@Time    :   2024/04/12 16:49:39
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import json
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    options_to_json,
    base64url_to_bytes,
    generate_authentication_options,
    verify_authentication_response
)
from webauthn.helpers.structs import RegistrationCredential
from webauthn.helpers.exceptions import InvalidRegistrationResponse, InvalidAuthenticationResponse
from sqlalchemy.orm import Session

from utils.db import get_db
from utils.model.api_schemas import WebauthnReg
from utils.model.orm import Passkeys, RegistrationAttempt, AuthSession, UserRegProcess
from utils.security import generate_jwt, verify_jwt, get_current_user

from env import RP_ID, RP_NAME, RP_SOURCE, DATABASE_URL

router = APIRouter(prefix='/auth', tags=['Authentication'])


class User(BaseModel):
    username: str = Field(
        pattern=r'^[a-zA-Z0-9_-]+$',
        min_length=3,
        max_length=16
    )


@router.post('/generate-registration-options', response_class=JSONResponse, response_model=WebauthnReg)
def start_registration(user: User, request: Request, db: Session = Depends(get_db)):
    user_agent = request.headers.get('user-agent', 'unknown')
    access_address = request.client.host
    go_find_user = db.query(UserRegProcess).filter_by(
        username=user.username).first()
    if go_find_user and go_find_user.finished_register:
        return WebauthnReg(status='CLIENT_ERROR', msg='UserAlreadyExist', payload=None)
    simple_registration_options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_name=user.username,
        user_display_name=user.username,
        user_id=user.username.encode('utf-8')
    )
    new_attempt = RegistrationAttempt(
        user=user.username,
        challenge=simple_registration_options.challenge,
        user_agent=user_agent,
        access_address=access_address
    )
    db.add(new_attempt)
    db.commit()
    return WebauthnReg(status='OK', msg='AllDone', payload=json.loads(options_to_json(simple_registration_options)))


@router.post('/verify-registration', response_class=JSONResponse, response_model=WebauthnReg)
def after_registration(response: dict, db: Session = Depends(get_db)):
    try:
        challenge = base64url_to_bytes(response["challenge"])
    except KeyError:
        return WebauthnReg(status='CLIENT_ERROR', msg='RequestNotUnderstandable', payload=None)
    att = db.query(RegistrationAttempt).filter_by(challenge=challenge).first()
    if att is None or att.created_at < datetime.now(timezone.utc) - timedelta(minutes=3):
        go_find_user = db.query(UserRegProcess).filter_by(
            username=att.user).first()
        db.delete(go_find_user)
        db.commit()
        return WebauthnReg(status='CLIENT_ERROR', msg='RegistrationTimeOut', payload=None)
    try:
        registration_verification = verify_registration_response(
            credential=response['payload'],
            expected_challenge=challenge,
            expected_origin=RP_SOURCE,
            expected_rp_id=RP_ID,
            require_user_verification=True
        )
        new_key = Passkeys(
            user=att.user,
            credential_id=registration_verification.credential_id,
            public_key=registration_verification.credential_public_key,
            device_type=registration_verification.credential_device_type.name,
            annotate="Passkey@" + att.access_address,
            transports=','.join(response['payload']['response']['transports']),
            sign_count=registration_verification.sign_count,
            registed_user_agent=att.user_agent,
            raw_id=response['payload']['rawId']
        )
        db.add(new_key)
        go_find_user.finished_register = True
    except InvalidRegistrationResponse as e:
        return WebauthnReg(status='CLIENT_ERROR', msg=str(e), payload=None)
    except Exception as e:
        raise e
    finally:
        db.delete(att)
        db.commit()
    return WebauthnReg(status='OK', msg='AllDone', payload=None)


@router.post('/generate-authentication-options', response_class=JSONResponse, response_model=WebauthnReg)
def start_authentication(db: Session = Depends(get_db)):
    simple_authentication_options = generate_authentication_options(
        rp_id=RP_ID)
    return WebauthnReg(status='OK', msg='AllDone', payload=json.loads(options_to_json(simple_authentication_options)))


@router.post('/verify-authentication', response_class=JSONResponse, response_model=WebauthnReg)
def after_authentication(response: dict, request: Request, db: Session = Depends(get_db)):
    passkey = db.query(Passkeys).filter_by(
        raw_id=response['payload']['rawId']).first()
    if passkey is None:
        return WebauthnReg(status='CLIENT_ERROR', msg='NoPublicKey', payload=None)
    try:
        authentication_verification = verify_authentication_response(
            credential=response['payload'],
            expected_challenge=base64url_to_bytes(response["challenge"]),
            expected_rp_id=RP_ID,
            expected_origin=RP_SOURCE,
            credential_public_key=passkey.public_key,
            credential_current_sign_count=passkey.sign_count,
            require_user_verification=True,
        )
        passkey.sign_count = authentication_verification.new_sign_count
        token, payload = generate_jwt(str(passkey.id), passkey.user)
        new_session = AuthSession(
            id=payload['jti'],
            user=passkey.user,
            source='LOGIN_SESSION',
            expiry_date=payload['exp'],
            is_active=True,
            user_agent=request.headers.get('user-agent', 'unknown'),
            related_passkey=passkey.id
        )
        db.add(new_session)
        db.commit()
        return WebauthnReg(status='OK', msg='AllDone', payload={'token': token})
    except InvalidAuthenticationResponse as e:
        return WebauthnReg(status='CLIENT_ERROR', msg=str(e), payload=None)
    except Exception as e:
        raise e


class AuthJWT(BaseModel):
    token: str


@router.post('/verify-jwt', response_class=JSONResponse, response_model=WebauthnReg)
def check_jwt(auth_jwt: AuthJWT, request: Request, db: Session = Depends(get_db)):
    res = verify_jwt(
        auth_jwt.token,
        request.headers.get('user-agent', 'unknown'),
        db=db
    )
    # TODO New token when expired
    if res:
        return WebauthnReg(status='OK', msg='AllDone', payload=None)
    else:
        return WebauthnReg(status='CLIENT_ERROR', msg='InvalidToken', payload=None)
