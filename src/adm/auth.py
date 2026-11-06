from litestar import Router, get, post, put, delete, Response
from dataclasses import dataclass

from litestar.di import NamedDependency
from litestar.params import JSONBody
from litestar.status_codes import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from models import Usuario
from sessao import Sessao
from sqlmodel import select


@dataclass
class LoginInfoModel:
    username: str
    password: str


@post('/login', status_code=HTTP_200_OK)
async def auth_login(data: JSONBody[LoginInfoModel], sessao: NamedDependency[Sessao]) -> Usuario|Response:
    qr = sessao.db.exec(
        select(Usuario)
        .where(Usuario.usuario == data.username,
               Usuario.senha == data.password)
    )
    res = qr.first()
    return res if res else Response(content='', status_code=HTTP_401_UNAUTHORIZED)


rota_auth = Router(
    path='/auth',
    route_handlers=[
        auth_login,
    ]
)
