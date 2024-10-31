import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from madr.app import app
from madr.db import get_session
from madr.models import Conta, Romancista, table_registry
from madr.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        poolclass=StaticPool,
        connect_args={'check_same_thread': False},
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


# @pytest.fixture(scope='session')
# def engine():
#     # with PostgresContainer('postgres:16', driver='psycopg') as postgres:
#     #     _engine = create_engine(postgres.get_connection_url())
#     #     with _engine.begin():
#     #         yield _engine
#     _engine = create_engine('sqlite:///:memory:')
#     return _engine


class ContaFactory(factory.Factory):
    class Meta:
        model = Conta

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}pass')


class RomancistaFactory(factory.Factory):
    class Meta:
        model = Romancista

    nome = factory.Sequence(lambda n: f'test {n}')


@pytest.fixture
def conta(session):
    senha = 'test'
    conta = ContaFactory(senha=get_password_hash(senha))
    session.add(conta)
    session.commit()
    session.refresh(conta)

    conta.senha_texto = senha

    return conta


@pytest.fixture
def outra_conta(session):
    senha = 'test'
    conta = ContaFactory(senha=get_password_hash(senha))
    session.add(conta)
    session.commit()
    session.refresh(conta)

    conta.senha_texto = senha

    return conta


@pytest.fixture
def romancista(session):
    romancista = RomancistaFactory()
    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


@pytest.fixture
def outro_romancista(session):
    romancista = RomancistaFactory()
    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


@pytest.fixture
def token(client, conta):
    resp = client.post(
        '/auth/token',
        data={'username': conta.email, 'password': conta.senha_texto},
    )
    return resp.json()['access_token']
