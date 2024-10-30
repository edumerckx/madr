from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from madr.db import get_session
from madr.models import Conta
from madr.schemas.auth import Token
from madr.security import create_token, get_current_conta, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[SessionORM, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token, status_code=HTTPStatus.CREATED)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    conta = session.scalar(
        select(Conta).where(Conta.email == form_data.username)
    )

    bad_request = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='Credenciais incorretas'
    )

    if not conta:
        raise bad_request

    if not verify_password(form_data.password, conta.senha):
        raise bad_request

    access_token = create_token(data={'sub': conta.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post(
    '/refresh-token', response_model=Token, status_code=HTTPStatus.CREATED
)
def refresh_token(conta: Conta = Depends(get_current_conta)):
    access_token = create_token(data={'sub': conta.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
