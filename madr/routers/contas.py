from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from madr.db import get_session
from madr.models import Conta
from madr.schemas.contas import ContaList, ContaResponse, ContaSchema
from madr.schemas.filters import FiltersPage

router = APIRouter(prefix='/contas', tags=['contas'])


@router.post('/', response_model=ContaResponse, status_code=HTTPStatus.CREATED)
def create_conta(conta: ContaSchema, session: Session = Depends(get_session)):
    db_conta = session.scalar(
        select(Conta).where(Conta.username == conta.username)
    )
    if db_conta:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Conta já registrada para este usuário',
        )

    new_conta = Conta(
        username=conta.username, email=conta.email, senha=conta.senha
    )

    session.add(new_conta)
    session.commit()
    session.refresh(new_conta)

    return new_conta


@router.get('/', response_model=ContaList, status_code=HTTPStatus.OK)
def get_contas(
    session: Session = Depends(get_session), filters: FiltersPage = Query()
):
    contas = session.scalars(
        select(Conta).offset(filters.offset).limit(filters.limit)
    ).all()
    return {'contas': contas}


@router.get(
    '/{conta_id}', response_model=ContaResponse, status_code=HTTPStatus.OK
)
def get_conta(conta_id: int, session: Session = Depends(get_session)):
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
    conta_id: int, conta: ContaSchema, session: Session = Depends(get_session)
):
    db_conta = session.scalar(select(Conta).where(Conta.id == conta_id))

    if not db_conta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Conta não encontrada',
        )

    try:
        db_conta.username = conta.username
        db_conta.email = conta.email
        db_conta.senha = conta.senha

        session.commit()
        session.refresh(db_conta)

        return db_conta
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username e/ou email já registrados',
        )


@router.delete('/{conta_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_conta(conta_id: int, session: Session = Depends(get_session)):
    db_conta = session.scalar(select(Conta).where(Conta.id == conta_id))

    if not db_conta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Conta não encontrada',
        )

    session.delete(db_conta)
    session.commit()
