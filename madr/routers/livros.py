from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from madr.db import get_session
from madr.models import Conta, Livro
from madr.schemas.filters import FiltersPage
from madr.schemas.livros import LivroList, LivroResponse, LivroSchema
from madr.security import get_current_conta

router = APIRouter(prefix='/livros', tags=['livros'])
Session = Annotated[SessionORM, Depends(get_session)]
CurrentConta = Annotated[Conta, Depends(get_current_conta)]


@router.get('/', response_model=LivroList, status_code=HTTPStatus.OK)
def get_livros(
    session: Session, conta: CurrentConta, filters: FiltersPage = Query()
):
    livros = session.scalars(
        select(Livro).offset(filters.offset).limit(filters.limit)
    ).all()
    return {'livros': livros}


@router.get(
    '/{livro_id}', response_model=LivroResponse, status_code=HTTPStatus.OK
)
def get_livro(livro_id: int, session: Session, conta: CurrentConta):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro nao encontrado',
        )

    return livro


@router.put(
    '/{livro_id}', response_model=LivroResponse, status_code=HTTPStatus.OK
)
def update_livro(
    livro_id: int, livro: LivroSchema, session: Session, conta: CurrentConta
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro nao encontrado',
        )

    db_livro.titulo = livro.titulo
    db_livro.ano = livro.ano
    db_livro.romancista_id = livro.romancista_id

    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.delete('/{livro_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_livro(livro_id: int, session: Session, conta: CurrentConta):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro nao encontrado',
        )

    session.delete(db_livro)
    session.commit()


@router.post('/', response_model=LivroResponse, status_code=HTTPStatus.CREATED)
def create_livro(session: Session, conta: CurrentConta, livro: LivroSchema):
    new_livro = Livro(
        titulo=livro.titulo, ano=livro.ano, romancista_id=livro.romancista_id
    )
    session.add(new_livro)
    session.commit()
    session.refresh(new_livro)
    return new_livro
