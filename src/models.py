from db import DBModel, FIntPK, get_engine, db_parameters, get_db_session
import os.path


class Usuario(DBModel, table=True):
    id: int = FIntPK()
    nome: str
    usuario: str
    senha: str


class Produto(DBModel, table=True):
    id: int = FIntPK()
    descricao: str
    preco: float


if not os.path.isfile(db_parameters['dbname']):
    # Cria a estrutura do banco
    engine = get_engine(echo=True)
    DBModel.metadata.create_all(engine)

    # Cria alguns registros iniciais
    session = get_db_session()
    session.add_all([
        Usuario(nome='Senhor Teste da Silva', usuario='teste', senha='123123'),
        Usuario(nome='Pirata \N{SKULL AND CROSSBONES}', usuario='\N{LOCK}', senha='\N{KEY}'),
        Produto(descricao='Produto X', preco=12.34),
        Produto(descricao='Produto \N{GREEK SMALL LETTER PI}', preco=3.14),
    ])
    session.commit()
