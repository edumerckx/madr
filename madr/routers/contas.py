from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionORM

from madr.db import get_session
from madr.models import Conta
from madr.schemas.contas import ContaList, ContaResponse, ContaSchema
from madr.schemas.filters import FiltersPage
from madr.security import get_current_conta, get_password_hash

router = APIRouter(prefix='/contas', tags=['contas'])

Session = Annotated[SessionORM, Depends(get_session)]
CurrentConta = Annotated[Conta, Depends(get_current_conta)]


@router.post('/', response_model=ContaResponse, status_code=HTTPStatus.CREATED)
def create_conta(conta: ContaSchema, session: Session):
    db_conta = session.scalar(
        select(Conta).where(Conta.username == conta.username)
    )
    if db_conta:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Conta já registrada para este usuário',
        )

    new_conta = Conta(
        username=conta.username,
        email=conta.email,
        senha=get_password_hash(conta.senha),
    )

    session.add(new_conta)
    session.commit()
    session.refresh(new_conta)

    return new_conta


@router.get('/', response_model=ContaList, status_code=HTTPStatus.OK)
def get_contas(session: Session, filters: FiltersPage = Query()):
    contas = session.scalars(
        select(Conta).offset(filters.offset).limit(filters.limit)
    ).all()
    return {'contas': contas}


@router.get(
    '/{conta_id}', response_model=ContaResponse, status_code=HTTPStatus.OK
)
def get_conta(conta_id: int, session: Session):
    conta = session.scalar(select(Conta).where(Conta.id == conta_id))

    if not conta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Conta não encontrada',
        )

    return conta


@router.put(
    '/{conta_id}', response_model=ContaResponse, status_code=HTTPStatus.OK
)
def update_conta(
    conta_id: int,
    conta: ContaSchema,
    session: Session,
    current_conta: CurrentConta,
):
    if current_conta.id != conta_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes'
        )

    try:
        current_conta.username = conta.username
        current_conta.email = conta.email
        current_conta.senha = get_password_hash(conta.senha)

        session.commit()
        session.refresh(current_conta)

        return current_conta
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username e/ou email já registrados',
        )


@router.delete('/{conta_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_conta(conta_id: int, session: Session, current_conta: CurrentConta):
    if current_conta.id != conta_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Permissões insuficientes'
        )

    session.delete(current_conta)
    session.commit()
