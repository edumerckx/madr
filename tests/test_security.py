from jwt import decode

from madr.security import create_token, get_password_hash, verify_password
from madr.settings import Settings

settings = Settings()


def test_create_token():
    data = {'test': 'test'}
    token = create_token(data)
    decoded = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert decoded['test'] == data['test']


def test_verify_password():
    senha = 'test'
    hashed = get_password_hash(senha)

    assert verify_password(senha, hashed)
    assert verify_password('wrong', hashed) is False
