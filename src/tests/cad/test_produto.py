from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_202_ACCEPTED, \
    HTTP_204_NO_CONTENT
from litestar.testing import TestClient


def test_prod_auth(api_noauth: TestClient[Litestar]) -> None:
    response = api_noauth.get('/cad/produto/1')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_prod_get_all(api: TestClient[Litestar]) -> None:
    response = api.get('/cad/produto/all')
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list)


def test_prod_get(api: TestClient[Litestar]) -> None:
    response = api.get('/cad/produto/1')
    assert response.status_code == HTTP_200_OK
    assert response.json()['id'] == 1


def test_prod_ins(api: TestClient[Litestar]) -> None:
    response = api.post('/cad/produto/', json={'descricao': 'novo prod', 'preco': 5})
    assert response.status_code == HTTP_201_CREATED
    novo = response.json()

    response = api.get(f'/cad/produto/{novo["id"]}')
    assert response.status_code == HTTP_200_OK
    assert response.json()['descricao'] == 'novo prod'


def test_prod_upd(api: TestClient[Litestar]) -> None:
    d = {'descricao': '_alterado_', 'preco': 5}
    response = api.put('/cad/produto/1', json=d)
    assert response.status_code == HTTP_202_ACCEPTED

    response = api.get(f'/cad/produto/1')
    assert response.status_code == HTTP_200_OK
    assert response.json()['descricao'] == d['descricao']

    response = api.put('/cad/produto/999999999', json=d)
    assert response.status_code == HTTP_204_NO_CONTENT
