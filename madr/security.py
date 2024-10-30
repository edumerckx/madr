from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM
from zoneinfo import ZoneInfo

from madr.db import get_session
from madr.models import Conta
from madr.schemas.auth import TokenData
from madr.settings import Settings

password_hash = PasswordHash.recommended()
settings = Settings()
OAuth2Scheme = Annotated[
    str, Depends(OAuth2PasswordBearer(tokenUrl='auth/token'))
]
Session = Annotated[SessionORM, Depends(get_session)]


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expires = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expires})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_current_conta(session: Session, token: OAuth2Scheme):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer...'},
    )

    try:
        payload = decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        username = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception

    conta = session.scalar(
        select(Conta).where(Conta.email == token_data.username)
    )
    if not conta:
        raise credentials_exception

    return conta
