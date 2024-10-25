from http import HTTPStatus


def test_create_conta(client):
    resp = client.post(
        '/contas/',
        json={'username': 'test', 'email': 'test@test.com', 'senha': 'test123'},
    )

    expected = {'id': 1, 'username': 'test', 'email': 'test@test.com'}
    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json() == expected


def test_create_conta_conflict(client, conta):
    resp = client.post(
        '/contas/',
        json={
            'username': conta.username,
            'email': 'test@test.com',
            'senha': 'test123',
        },
    )

    assert resp.status_code == HTTPStatus.CONFLICT
    assert resp.json() == {'detail': 'Conta já registrada para este usuário'}


def test_get_contas_empty(client):
    resp = client.get(
        '/contas/',
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {'contas': []}


def test_get_contas(client, conta):
    resp = client.get(
        '/contas/',
    )

    data = resp.json()

    assert resp.status_code == HTTPStatus.OK
    assert 'contas' in data
    assert data['contas'][0]['username'] == conta.username
    assert data['contas'][0]['id'] == conta.id
    assert data['contas'][0]['email'] == conta.email


def test_get_conta(client, conta):
    resp = client.get(
        f'/contas/{conta.id}',
    )

    expected = {
        'id': conta.id,
        'username': conta.username,
        'email': conta.email,
    }

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == expected


def test_get_conta_not_found(client):
    resp = client.get(
        '/contas/999',
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json() == {'detail': 'Conta não encontrada'}


def test_update_conta(client, conta, token):
    data = {
        'username': 'update_test',
        'email': 'update@test.com',
        'senha': 'test',
    }

    expected = {
        'id': conta.id,
        'username': 'update_test',
        'email': 'update@test.com',
    }

    resp = client.put(
        f'/contas/{conta.id}',
        json=data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == expected


def test_update_conta_forbidden(client, token):
    data = {'username': 'test', 'email': 'test@test.com', 'senha': 'test'}

    resp = client.put(
        '/contas/999', json=data, headers={'Authorization': f'Bearer {token}'}
    )

    assert resp.status_code == HTTPStatus.FORBIDDEN
    assert resp.json() == {'detail': 'Permissões insuficientes'}


def test_update_conta_conflict(client, conta, outra_conta, token):
    data = {
        'username': outra_conta.username,
        'email': outra_conta.email,
        'senha': 'test',
    }

    resp = client.put(
        f'/contas/{conta.id}',
        json=data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.CONFLICT
    assert resp.json() == {'detail': 'Username e/ou email já registrados'}


def test_delete_conta(client, conta, token):
    resp = client.delete(
        f'/contas/{conta.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT
    assert resp.content == b''


def test_delete_conta_forbidden(client, token):
    resp = client.delete(
        '/contas/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.FORBIDDEN
    assert resp.json() == {'detail': 'Permissões insuficientes'}
