from http import HTTPStatus


def test_create_romancista(client, token):
    resp = client.post(
        '/romancistas/',
        json={'nome': 'test'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json() == {'id': 1, 'nome': 'test'}


def test_create_romancista_conflict(client, romancista, token):
    resp = client.post(
        '/romancistas/',
        json={'nome': romancista.nome},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.CONFLICT
    assert resp.json() == {'detail': 'Romancista já registrado'}


def test_get_romancistas(client, romancista, token):
    resp = client.get(
        '/romancistas/',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = resp.json()

    assert resp.status_code == HTTPStatus.OK
    assert len(data)
    assert 'romancistas' in data
    assert 'nome' in data['romancistas'][0]


def test_get_romancistas_empty(client, token):
    resp = client.get(
        '/romancistas/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {'romancistas': []}


def test_get_romancista(client, romancista, token):
    resp = client.get(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {'id': romancista.id, 'nome': romancista.nome}


def test_get_romancista_not_found(client, token):
    resp = client.get(
        '/romancistas/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json() == {'detail': 'Romancista não encontrado'}


def test_update_romancista(client, romancista, token):
    expected = {'id': romancista.id, 'nome': f'{romancista.nome} update'}

    resp = client.put(
        f'/romancistas/{romancista.id}',
        json={'nome': f'{romancista.nome} update'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == expected


def test_update_romancista_not_found(client, token):
    resp = client.put(
        '/romancistas/999',
        json={'nome': 'update'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json() == {'detail': 'Romancista não encontrado'}


def test_update_romancista_conflict(
    client, romancista, outro_romancista, token
):
    resp = client.put(
        f'/romancistas/{romancista.id}',
        json={'nome': outro_romancista.nome},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.CONFLICT
    assert resp.json() == {'detail': 'Romancista já registrado'}


def test_delete_romancista(client, romancista, token):
    resp = client.delete(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_delete_romancista_not_found(client, token):
    resp = client.delete(
        '/romancistas/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json() == {'detail': 'Romancista não encontrado'}
