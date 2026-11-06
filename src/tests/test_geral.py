from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_202_ACCEPTED, \
    HTTP_204_NO_CONTENT
from litestar.testing import TestClient


def test_sessinfo_auth(api: TestClient[Litestar]) -> None:
    response = api.get('/info')
    assert response.status_code == HTTP_200_OK
    assert response.json()['usuario_id'] == 1


def test_sessinfo_noauth(api_noauth: TestClient[Litestar]) -> None:
    response = api_noauth.get('/info')
    assert response.status_code == HTTP_200_OK
    assert response.json()['usuario_id'] == 0