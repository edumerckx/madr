from http import HTTPStatus

from tests.conftest import LivroFactory


def test_get_livros_empty(client, token):
    resp = client.get(
        '/livros/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {'livros': []}


def test_get_livros(client, livro, token):
    resp = client.get(
        '/livros/',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = resp.json()

    assert resp.status_code == HTTPStatus.OK
    assert len(data)
    assert 'livros' in data


def test_list_livros_should_return_2_livros(client, token, session, romancista):
    session.bulk_save_objects(
        LivroFactory.create_batch(5, romancista_id=romancista.id)
    )
    session.commit()

    resp = client.get(
        '/livros/?limit=2&offset=0',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = resp.json()['livros']
    expected_length = 2

    assert resp.status_code == HTTPStatus.OK
    assert len(data) == expected_length


def test_get_livro(client, livro, token):
    resp = client.get(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected = {
        'id': livro.id,
        'titulo': livro.titulo,
        'ano': livro.ano,
        'romancista_id': livro.romancista_id,
    }

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == expected


def test_get_livro_not_found(client, token):
    resp = client.get(
        '/livros/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json() == {'detail': 'Livro nao encontrado'}


def test_update_livro(client, livro, token):
    resp = client.put(
        f'/livros/{livro.id}',
        json={'titulo': 'update', 'ano': 2001, 'romancista_id': 1},
        headers={'Authorization': f'Bearer {token}'},
    )

    expected = {
        'id': livro.id,
        'titulo': 'update',
        'ano': 2001,
        'romancista_id': livro.romancista_id,
    }

    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == expected


def test_update_livro_not_found(client, token):
    resp = client.put(
        '/livros/999',
        json={'titulo': 'update', 'ano': 2001, 'romancista_id': 1},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json() == {'detail': 'Livro nao encontrado'}


def test_delete_livro(client, livro, token):
    resp = client.delete(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_delete_livro_not_found(client, token):
    resp = client.delete(
        '/livros/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json() == {'detail': 'Livro nao encontrado'}


def test_create_livro(client, token, romancista):
    resp = client.post(
        '/livros/',
        json={'titulo': 'test', 'ano': 2001, 'romancista_id': romancista.id},
        headers={'Authorization': f'Bearer {token}'},
    )

    excepted = {
        'id': 1,
        'titulo': 'test',
        'ano': 2001,
        'romancista_id': romancista.id,
    }

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json() == excepted
