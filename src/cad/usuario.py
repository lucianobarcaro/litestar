from typing import List

from litestar import Router, get, post, put, Response
from litestar.di import NamedDependency
from litestar.params import JSONBody, FromPath
from litestar.status_codes import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED
from sqlmodel import select

from guards import autenticado
from models import Usuario
from sessao import Sessao


@get('/all')
async def get_usuario_all(sessao: NamedDependency[Sessao]) -> List[Usuario]:
    rows = sessao.db.exec(select(Usuario)).all()
    return rows


@get('/{id_usuario:int}')
async def get_usuario(id_usuario: FromPath[int], sessao: NamedDependency[Sessao]) -> Usuario | Response:
    qr = sessao.db.exec(
        select(Usuario)
        .where(Usuario.id == id_usuario)
    )
    res = qr.first()
    return res if res else Response(content='', status_code=HTTP_204_NO_CONTENT)


@post('/')
async def ins_usuario(data: JSONBody[Usuario], sessao: NamedDependency[Sessao]) -> dict:
    sessao.db.add(data)
    sessao.db.commit()
    return {'id': data.id}


@put('/{id_usuario:int}', status_code=HTTP_202_ACCEPTED)
async def upd_usuario(id_usuario: FromPath[int], data: JSONBody[Usuario], sessao: NamedDependency[Sessao]) -> bool | Response:
    r = sessao.db.get(Usuario, id_usuario)
    if not r:
        return Response('', status_code=HTTP_204_NO_CONTENT)

    r.nome = data.nome
    r.usuario = data.usuario
    r.senha = data.senha
    sessao.db.commit()

    return True


rota_cad_usuario = Router(
    path='/cad/usuario',
    route_handlers=[
        get_usuario_all,
        get_usuario,
        ins_usuario,
        upd_usuario
    ],
    guards=[autenticado]
)
