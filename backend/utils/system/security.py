# -*- encoding: utf-8 -*-
'''
security.py
----
安全相关的内容


@Time    :   2024/04/15 11:44:37
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import jwt
import aiofiles
from pathlib import Path
import uuid
from typing import Tuple, Any
from datetime import datetime, timedelta, timezone
from fastapi import Depends, Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from utils.db import get_db
from env import RP_ID
from utils.model.orm import Passkeys, RegistrationAttempt, AuthSession, Permission
import cryptography
from cryptography.hazmat.primitives.asymmetric import ec
from utils.logger import logger

security = HTTPBearer()


class UserSession(BaseModel):
    user: str
    session: uuid.UUID


async def get_current_user_session(
    authentication: HTTPAuthorizationCredentials = Security(security),
    user_agent: str = Header(...),
    db: AsyncSession = Depends(get_db)
) -> UserSession:
    data = await verify_jwt(authentication.credentials,
                            user_agent, db, return_info=True)
    if not data:
        raise HTTPException(status_code=401)
    return UserSession(**data)


async def permission_check(user: str, permission_node: str, db: AsyncSession) -> bool:
    async with db as session:
        result = await session.execute(
            select(Permission).filter_by(user=user, permission=permission_node)
        )
        permission = result.scalars().one_or_none()
        return permission is not None


class RequirePermission:
    def __init__(self, permission_node: str):
        self.permission_node = permission_node

    async def __call__(self, user_session: UserSession = Depends(get_current_user_session), db: AsyncSession = Depends(get_db)):
        if not await permission_check(user_session.user, self.permission_node, db):
            raise HTTPException(status_code=401)


def generate_jwt(secrets: str, user_id: str) -> tuple[str, dict]:
    payload = {
        'iss': RP_ID,
        'sub': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=48),
        'iat': datetime.now(timezone.utc),
        'jti': str(uuid.uuid4())
    }
    token = jwt.encode(payload, secrets, algorithm='HS256')
    return token, payload


async def verify_jwt(
        jwt_str: str,
        ua: str,
        db: AsyncSession,
        return_info=False
):
    logger.debug(f'Verifying JWT: {jwt_str}')
    try:
        res = jwt.decode(jwt_str, algorithms=['HS256'], options={
                         'verify_signature': False})
    except Exception:
        logger.debug('JWT Decryption Failed')
        return False

    try:
        result = await db.execute(select(AuthSession).filter_by(id=res['jti']))
        current_session = result.scalars().first()
        if current_session is None:
            logger.debug('Session Not Found')
            return False

        result = await db.execute(select(Passkeys).filter_by(id=current_session.related_passkey))
        passkey = result.scalars().first()
        if not passkey:
            logger.debug('Passkey Not Found')
            return False
    except Exception:
        logger.debug('Database Error')
        return False

    try:
        res = jwt.decode(jwt_str, algorithms=[
                         'HS256'], key=str(passkey.user_secret))
    except:
        logger.debug('JWT Signature Verification Failed')
        return False

    if current_session.user_agent != ua:
        logger.debug('User Agent Mismatch')
        return False

    if return_info:
        return {
            'user': res['sub'],
            'session': current_session.id
        }

    return True


def generate_ecc_key_pair() -> Tuple[str, str]:
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    private_key_pem = private_key.private_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
        format=cryptography.hazmat.primitives.serialization.PrivateFormat.PKCS8,
        encryption_algorithm=cryptography.hazmat.primitives.serialization.NoEncryption()
    ).decode('utf-8')
    public_key_pem = public_key.public_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
        format=cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    return private_key_pem, public_key_pem


async def async_load_key_pair() -> Tuple[str, str]:
    private_key_path = Path('private_key.pem')
    public_key_path = Path('public_key.pem')
    if not private_key_path.is_file() or not public_key_path.is_file():
        private_key, public_key = generate_ecc_key_pair()
        async with aiofiles.open(private_key_path, 'w') as f:
            await f.write(private_key)
        async with aiofiles.open(public_key_path, 'w') as f:
            await f.write(public_key)
    else:
        async with aiofiles.open(private_key_path, 'r') as f:
            private_key = await f.read()
        async with aiofiles.open(public_key_path, 'r') as f:
            public_key = await f.read()
    return private_key, public_key


def sync_load_key_pair() -> Tuple[str, str]:
    private_key_path = Path('private_key.pem')
    public_key_path = Path('public_key.pem')
    if not private_key_path.is_file() or not public_key_path.is_file():
        private_key, public_key = generate_ecc_key_pair()
        with open(private_key_path, 'w') as f:
            f.write(private_key)
        with open(public_key_path, 'w') as f:
            f.write(public_key)
    else:
        with open(private_key_path, 'r') as f:
            private_key = f.read()
        with open(public_key_path, 'r') as f:
            public_key = f.read()
    return private_key, public_key
