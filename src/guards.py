from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler
from sessao import cache


async def autenticado(connection: ASGIConnection, handler: BaseRouteHandler):
    s = cache.get()
    if not s or s.usuario_id == 0:
        raise NotAuthorizedException(detail='Usuário não autenticado')
