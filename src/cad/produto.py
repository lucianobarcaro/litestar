from typing import List

from litestar import Router, get, post, put, Response
from litestar.di import NamedDependency
from litestar.params import JSONBody, FromPath
from litestar.status_codes import HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from sqlmodel import select

from guards import autenticado
from models import Produto
from sessao import Sessao


@get('/all')
async def get_produto_all(sessao: NamedDependency[Sessao]) -> List[Produto]:
    rows = sessao.db.exec(select(Produto)).all()
    return rows


@get('/{id_produto:int}')
async def get_produto(id_produto: FromPath[int], sessao: NamedDependency[Sessao]) -> Produto | Response:
    r = sessao.db.get(Produto, id_produto)
    return r if r else Response('', status_code=204)


@post('/')
async def ins_produto(data: JSONBody[Produto], sessao: NamedDependency[Sessao]) -> dict:
    sessao.db.add(data)
    sessao.db.commit()
    return {'id': data.id}


@put('/{id_produto:int}', status_code=HTTP_202_ACCEPTED)
async def upd_produto(id_produto: FromPath[int], data: JSONBody[Produto], sessao: NamedDependency[Sessao]) -> bool | Response:
    r = sessao.db.get(Produto, id_produto)
    if not r:
        return Response('', status_code=HTTP_204_NO_CONTENT)

    r.descricao = data.descricao
    r.preco = data.preco
    sessao.db.commit()

    return True


rota_cad_produto = Router(
    path='/cad/produto',
    route_handlers=[
        get_produto_all,
        get_produto,
        ins_produto,
        upd_produto,
    ],
    guards=[autenticado]
)
