# -*- encoding: utf-8 -*-
'''
db.py
----
put some words here


@Time    :   2024/04/13 17:11:28
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

import enum
import uuid
import secrets
import string
from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, String, DateTime, Boolean, Text, BigInteger, Float
from sqlalchemy.dialects.postgresql import UUID, BYTEA, BIT, JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.types import Enum

from env import DATABASE_URL


Base = declarative_base()
engine = create_engine(DATABASE_URL)


def generate_secret(length=32) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    client_secret = ''.join(secrets.choice(alphabet) for i in range(length))
    return client_secret


class Passkeys(Base):
    __tablename__ = 'auth_passkeys'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user = Column(String, nullable=False, index=True)
    raw_id = Column(String, nullable=False, unique=True, index=True)
    credential_id = Column(BYTEA, nullable=False, unique=True)
    public_key = Column(BYTEA, nullable=False)
    sign_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
    device_type = Column(String)
    annotate = Column(String)
    backed_up = Column(Boolean, default=False)
    transports = Column(String)
    registed_user_agent = Column(String)
    user_secret = Column(String, default=generate_secret(48))
    is_deleted = Column(Boolean, default=False)
    deleted_by = Column(String)


class RegistrationAttempt(Base):
    __tablename__ = 'auth_registration_attempts'

    challenge = Column(BYTEA, primary_key=True)
    user = Column(String, nullable=False, index=True)
    user_agent = Column(String, nullable=False)
    access_address = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuthSession(Base):
    __tablename__ = 'auth_sessions'
    id = Column(UUID, primary_key=True)
    user = Column(String, nullable=False, index=True)
    source = Column(String, nullable=False)
    related_passkey = Column(UUID, nullable=False)
    expiry_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())


class Permission(Base):
    __tablename__ = 'auth_permissions'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user = Column(String, nullable=False, index=True)
    permission = Column(String, nullable=False, index=True)
    operation_log_id = Column(BigInteger, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())


class OperationLog(Base):
    __tablename__ = 'log_operations'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False, index=True, default='**MOSSY_ROOT**')
    operation_time = Column(DateTime(timezone=True),
                            index=True, default=func.now())
    related_session = Column(UUID, nullable=False, index=True,
                             default='00000000-0000-0000-0000-000000000000')
    module = Column(String, nullable=False, index=True)
    operation = Column(JSONB, nullable=False, index=True)


class ErrorLog(Base):
    __tablename__ = 'log_exceptions'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    node_id = Column(UUID, index=True)
    worker_id = Column(UUID)
    error_time = Column(DateTime(timezone=True), default=func.now())
    error_message = Column(String, index=True)
    error_type = Column(String, index=True)
    error_stack = Column(Text)


class UserRegProcess(Base):
    __tablename__ = 'auth_user_register_process'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    finished_register = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())


class SystemConfig(Base):
    __tablename__ = 'system_config'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())


class UserConfig(Base):
    __tablename__ = 'user_config'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False, index=True)
    key = Column(String, nullable=False, index=True)
    value = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
    __table_args__ = (
        UniqueConstraint('user', 'key', name='uq_user_key'),
    )


class NodeType(enum.Enum):
    fastapi = "FASTAPI"
    backgrounder = "CELERY-WORKER"
    scheduler = "CELERY-BEAT"


class NodeInfo(Base):
    __tablename__ = 'node_info'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    node_id = Column(UUID, default=uuid.uuid4, index=True)
    node_type = Column(Enum(NodeType))
    cpus = Column(Integer)
    mem_in_gb = Column(Float)
    node_name = Column(String)
    ipv4 = Column(String)
    ipv6 = Column(String)
    remark = Column(String)
    public_key = Column(String)
    activated = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('node_id', 'node_type', name='uq_node_type'),
    )


class OAuthApp(Base):
    __tablename__ = 'oauth_apps'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    client_id = Column(UUID, default=uuid.uuid4, unique=True)
    client_secret = Column(String, nullable=False,
                           default=generate_secret(48))
    name = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)
    scopes = Column(String)
    website = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())


class OAuthAuthorizationCode(Base):
    __tablename__ = 'oauth_authorization_codes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False,
                  default=generate_secret(24))
    client_id = Column(UUID, nullable=False)
    redirect_uri = Column(String, nullable=False)
    scopes = Column(String)
    user = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class OAuthAccessToken(Base):
    __tablename__ = 'oauth_access_tokens'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    token = Column(String, unique=True, nullable=False)
    client_id = Column(UUID, nullable=False)
    user = Column(String, nullable=False)
    scopes = Column(String)
    note = Column(String)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
