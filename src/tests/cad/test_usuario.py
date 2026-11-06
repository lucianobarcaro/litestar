from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_202_ACCEPTED, \
    HTTP_204_NO_CONTENT
from litestar.testing import TestClient


def test_usuario_auth(api_noauth: TestClient[Litestar]) -> None:
    response = api_noauth.get('/cad/usuario/1')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_usuario_get_all(api: TestClient[Litestar]) -> None:
    response = api.get('/cad/usuario/all')
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list)


def test_usuario_get(api: TestClient[Litestar]) -> None:
    response = api.get('/cad/usuario/1')
    assert response.status_code == HTTP_200_OK
    assert response.json()['id'] == 1


def test_usuario_ins(api: TestClient[Litestar]) -> None:
    response = api.post('/cad/usuario/', json={'nome': 'novo', 'usuario': 'xxx', 'senha': 'yyy'})
    assert response.status_code == HTTP_201_CREATED
    novo = response.json()

    response = api.get(f'/cad/usuario/{novo["id"]}')
    assert response.status_code == HTTP_200_OK
    assert response.json()['nome'] == 'novo'


def test_usuario_upd(api: TestClient[Litestar]) -> None:
    d = {'nome': '_alterado_', 'usuario': 'xxx', 'senha': 'yyy'}
    response = api.put('/cad/usuario/1', json=d)
    assert response.status_code == HTTP_202_ACCEPTED

    response = api.get(f'/cad/usuario/1')
    assert response.status_code == HTTP_200_OK
    assert response.json()['nome'] == d['nome']

    response = api.put('/cad/usuario/999999999', json=d)
    assert response.status_code == HTTP_204_NO_CONTENT
