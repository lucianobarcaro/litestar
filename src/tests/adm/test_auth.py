from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from litestar.testing import TestClient


def test_auth_ok(api_noauth: TestClient[Litestar]) -> None:
    response = api_noauth.post('/auth/login', json={'username': 'teste', 'password': '123123'})
    assert response.status_code == HTTP_200_OK

def test_auth_err(api_noauth: TestClient[Litestar]) -> None:
    response = api_noauth.post('/auth/login', json={'username': 'teste', 'password': 'invalido'})
    assert response.status_code == HTTP_401_UNAUTHORIZED
