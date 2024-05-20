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
from typing import List
from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, String, DateTime, Boolean, Text, BigInteger, Float
from sqlalchemy.dialects.postgresql import UUID, BYTEA, BIT, JSONB, ARRAY
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


class AuthChallenges(Base):
    __tablename__ = 'auth_challenges'

    uuid = Column(UUID, default=uuid.uuid4, primary_key=True)
    user = Column(String, index=True)
    challenge = Column(BYTEA, nullable=False)
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


class ServerRules(Base):
    __tablename__ = 'rules'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
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


class MossyUser(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    identifier = Column(UUID(as_uuid=True), default=uuid.uuid4,
                        nullable=False, unique=True)
    fedi_account_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    preferred_language = Column(String)
    supported_languages = Column(ARRAY(String))
    registration_source = Column(String)
    recovery_key = Column(String, nullable=False, default='NO_RECOVERY_KEY')


class FediAccounts(Base):
    __tablename__ = 'fedi_accounts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, index=True)
    domain = Column(String, index=True)
    private_key = Column(String)
    public_key = Column(String, nullable=False)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True),
                       server_default=func.now(), onupdate=func.now())
    description = Column(String, index=True)
    description_in_markdown = Column(String)
    display_name = Column(String, index=True)
    uri = Column(String, index=True)
    url = Column(String, index=True)
    avatar_file_content = Column(String)
    avatar_file_type = Column(String)
    avatar_file_size = Column(BigInteger)
    avatar_update_at = Column(DateTime(timezone=True))
    header_file_content = Column(String)
    header_file_type = Column(String)
    header_file_size = Column(BigInteger)
    header_update_at = Column(DateTime(timezone=True))
    locked = Column(Boolean, default=False)
    last_webfingered_at = Column(DateTime(timezone=True))
    inbox_url = Column(String)
    outbox_url = Column(String)
    shared_inbox_url = Column(String)
    followers_url = Column(String)
    memorial = Column(Boolean, default=False)
    moved_to_account_id = Column(BigInteger)
    fields = Column(JSONB)
    actor_type = Column(String, index=True, nullable=False, default='Person')
    discoverable = Column(Boolean, default=True)
    also_known_as = Column(ARRAY(String))
    silenced_at = Column(DateTime(timezone=True))
    suspended_at = Column(DateTime(timezone=True))
    hide_collections = Column(Boolean, default=False)
    devices_url = Column(String)
    sensitized_at = Column(DateTime(timezone=True))
    trendable = Column(Boolean, default=True)
    indexable = Column(Boolean, default=True)
