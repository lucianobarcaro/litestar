from litestar import Router, get, post, put, Response
from litestar.params import JSONBody
from litestar.status_codes import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED
from sqlmodel import select

from guards import autenticado
from models import Usuario
from sessao import Sessao


@get('/{id_usuario:int}')
async def get_usuario(id_usuario: int, sessao: Sessao) -> Usuario | Response:
    qr = sessao.db.exec(
        select(Usuario)
        .where(Usuario.id == id_usuario)
    )
    res = qr.first()
    return res if res else Response(content='', status_code=HTTP_204_NO_CONTENT)


@post('/')
async def ins_usuario(data: JSONBody[Usuario], sessao: Sessao) -> dict:
    sessao.db.add(data)
    sessao.db.commit()
    return {'id': data.id}


@put('/{id_usuario:int}', status_code=HTTP_202_ACCEPTED)
async def upd_usuario(id_usuario: int, data: JSONBody[Usuario], sessao: Sessao) -> bool | Response:
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
        get_usuario,
        ins_usuario,
        upd_usuario
    ],
    guards=[autenticado]
)
