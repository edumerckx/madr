from http import HTTPStatus

from freezegun import freeze_time


def test_create_token(client, conta):
    data = {'username': conta.email, 'password': conta.senha_texto}

    resp = client.post('/auth/token', data=data)
    token = resp.json()

    assert resp.status_code == HTTPStatus.CREATED
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'


def test_create_token_wrong_password(client, conta):
    data = {
        'username': conta.email,
        'password': f'{conta.senha_texto}errada',
    }

    resp = client.post('/auth/token', data=data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json() == {'detail': 'Credenciais incorretas'}


def test_create_token_non_existent(client):
    data = {'username': 'test@test.com', 'password': 'test'}

    resp = client.post('/auth/token', data=data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json() == {'detail': 'Credenciais incorretas'}


def test_token_expired(client, conta):
    with freeze_time('2024-01-01 08:00:00'):
        resp = client.post(
            '/auth/token',
            data={'username': conta.email, 'password': conta.senha_texto},
        )
        assert resp.status_code == HTTPStatus.CREATED
        token = resp.json()['access_token']

    with freeze_time('2024-01-01 10:00:00'):
        resp = client.post(
            '/auth/refresh-token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert resp.status_code == HTTPStatus.UNAUTHORIZED
        assert resp.json() == {
            'detail': 'Não foi possível validar as credenciais'
        }


def test_refresh_token(client, conta, token):
    resp = client.post(
        '/auth/refresh-token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = resp.json()

    assert resp.status_code == HTTPStatus.CREATED
    assert 'access_token' in data
    assert 'token_type' in data
