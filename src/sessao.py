from typing import Any, Optional
from dataclasses import dataclass
from contextvars import ContextVar
from litestar import Request


@dataclass
class Sessao:
    db: Any
    usuario_id: Optional[int] = None

cache = ContextVar('sessao')  # , default=Sessao(db=None, usuario_id=None))


async def pega_sessao(request: Request) -> Sessao:
    return cache.get()
