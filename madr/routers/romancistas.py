from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionORM

from madr.db import get_session
from madr.models import Romancista
from madr.schemas.filters import FiltersPage
from madr.schemas.romancistas import (
    RomancistaList,
    RomancistaResponse,
    RomancistaSchema,
)
from madr.security import get_current_conta

router = APIRouter(prefix='/romancistas', tags=['romancistas'])
Session = Annotated[SessionORM, Depends(get_session)]
CurrentConta = Annotated[Romancista, Depends(get_current_conta)]


@router.post(
    '/', response_model=RomancistaResponse, status_code=HTTPStatus.CREATED
)
def create_romancista(
    romancista: RomancistaSchema, session: Session, conta: CurrentConta
):
    new_romancista = Romancista(nome=romancista.nome)
    try:
        session.add(new_romancista)
        session.commit()
        session.refresh(new_romancista)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já registrado',
        )

    return new_romancista


@router.get('/', response_model=RomancistaList, status_code=HTTPStatus.OK)
def get_romancistas(
    session: Session, conta: CurrentConta, filters: FiltersPage = Query()
):
    romancistas = session.scalars(
        select(Romancista).offset(filters.offset).limit(filters.limit)
    ).all()
    return {'romancistas': romancistas}


@router.get(
    '/{romancista_id}',
    response_model=RomancistaResponse,
    status_code=HTTPStatus.OK,
)
def get_romancista(romancista_id: int, conta: CurrentConta, session: Session):
    romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado',
        )

    return romancista


@router.put(
    '/{romancista_id}',
    response_model=RomancistaResponse,
    status_code=HTTPStatus.OK,
)
def update_romancista(
    romancista_id: int,
    romancista: RomancistaSchema,
    conta: CurrentConta,
    session: Session,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado',
        )

    try:
        db_romancista.nome = romancista.nome
        session.commit()
        session.refresh(db_romancista)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já registrado',
        )

    return db_romancista


@router.delete('/{romancista_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_romancista(
    romancista_id: int, conta: CurrentConta, session: Session
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado',
        )

    session.delete(db_romancista)
    session.commit()
