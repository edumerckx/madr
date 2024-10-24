from http import HTTPStatus


def test_create_token(client, conta):
    data = {'username': conta.username, 'password': conta.senha_texto}

    resp = client.post('/auth/token', data=data)
    token = resp.json()

    assert resp.status_code == HTTPStatus.CREATED
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'


def test_create_token_wrong_password(client, conta):
    data = {
        'username': conta.username,
        'password': f'{conta.senha_texto}errada',
    }

    resp = client.post('/auth/token', data=data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json() == {'detail': 'Credenciais incorretas'}


def test_create_token_non_existent(client):
    data = {'username': 'test', 'password': 'test'}

    resp = client.post('/auth/token', data=data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json() == {'detail': 'Credenciais incorretas'}
