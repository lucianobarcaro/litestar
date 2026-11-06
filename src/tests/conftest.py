from typing import TYPE_CHECKING
from collections.abc import Iterator
import pytest
from litestar.testing import TestClient
from init import app


if TYPE_CHECKING:
    from litestar import Litestar


@pytest.fixture(scope="module")
def api_noauth() -> Iterator[TestClient[Litestar]]:
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="module")
def api() -> Iterator[TestClient[Litestar]]:
    with TestClient(app=app) as client:
        client.headers["X-Usuario"] = '1'
        yield client
