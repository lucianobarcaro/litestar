from litestar import Litestar, get
from litestar.enums import ScopeType
from litestar.middleware import ASGIMiddleware
from litestar.config.cors import CORSConfig
from litestar.types import ASGIApp, Receive, Scope, Send
import asyncio

from adm.auth import rota_auth
from cad.produto import rota_cad_produto
from litestar.di import Provide
from sessao import Sessao, cache, pega_sessao
from cad.usuario import rota_cad_usuario
from db import get_db_session

cors_config = CORSConfig(allow_origins=["*"])


class TimeoutMiddleware(ASGIMiddleware):
    scopes = (ScopeType.HTTP,)
    exclude_path_pattern = r"^/schema"

    async def handle(self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp) -> None:
        await asyncio.wait_for(next_app(scope, receive, send), timeout=30)


class SessionMiddleware(ASGIMiddleware):
    scopes = (ScopeType.HTTP,)
    exclude_path_pattern = r"^/schema"

    async def handle(self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp) -> None:
        req_headers = {k.decode("latin1").lower(): v.decode("latin1") for k, v in scope.get("headers", [])}
        sess = Sessao(
            db=get_db_session(),
            usuario_id=int(req_headers.get("x-usuario", '0')),
        )
        sess_token = cache.set(sess)
        await next_app(scope, receive, send)
        cache.reset(sess_token)


@get('/info')
async def sess_info(sessao: Sessao) -> dict:
    return {
        'db': id(sessao.db),
        'usuario_id': sessao.usuario_id,
    }


app = Litestar(
    route_handlers=[
        rota_cad_produto,
        rota_cad_usuario,
        rota_auth,
        sess_info
    ],
    middleware=[
        SessionMiddleware(),
        TimeoutMiddleware(),
    ],
    cors_config=cors_config,
    dependencies={'sessao': Provide(pega_sessao)},
    debug=True
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
