"""
Tudo relacionado ao banco
"""

from sqlmodel import SQLModel, create_engine, Session
import pickle
import uuid
from sqlalchemy import JSON, Engine
from sqlalchemy import UUID, String, Integer, TIMESTAMP
# from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func
from sqlalchemy.types import UserDefinedType
from sqlmodel import Field

db_parameters = {
    'driver': 'sqlite',
    'dbname': './database.db'
}


def get_engine(**kwargs) -> Engine:
    return create_engine('{driver}:///{dbname}'.format(**db_parameters), **kwargs)


def get_db_session() -> Session:
    engine = get_engine()
    session = Session(bind=engine, expire_on_commit=False)

    # Criação de atalhos úteis
    session.cursor = lambda *args, **kwargs: session.connection().connection.cursor(*args, **kwargs)  # noqa
    session.db_name = lambda: session.connection().connection.driver_connection.database

    return session


class DBModel(SQLModel):
    # noinspection PyMethodParameters
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        tn = cls.__name__
        return "".join(
            ("_" if i > 0 and x.isupper() and tn[i - 1].islower() else "") + x.lower()
            for i, x in enumerate(tn)
        )


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)
            return Mutable.coerce(key, value)
        return value

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.changed()

    def clear(self):
        dict.clear(self)
        self.changed()


class PickleField(UserDefinedType):
    def get_col_spec(self):  # noqa
        return "LongBlob"

    def bind_processor(self, dialect):
        def processa(value):
            if type(value) is MutableDict:
                value = dict(value)
            return pickle.dumps(value)

        return processa

    def result_processor(self, dialect, coltype):
        def processa(value):
            try:
                return pickle.loads(value)
            except (TypeError, pickle.UnpicklingError):
                return None

        return processa


# noinspection PyPep8Naming
def FIntPK(**kwargs):
    # noinspection PyTypeChecker
    return Field(
        primary_key=True,
        default=None,
        sa_type=Integer,
        **kwargs
    )

# noinspection PyPep8Naming
def FJson(default_factory=lambda: {}, **kwargs):
    # noinspection PyTypeChecker
    return Field(
        default_factory=default_factory,
        sa_type=MutableDict.as_mutable(JSON()),
        **kwargs
    )


# noinspection PyPep8Naming
def FKUuid4(**kwargs):
    # noinspection PyTypeChecker
    return Field(
        sa_type=UUID(),
        sa_column_kwargs={"server_default": func.uuid_v4(), "index": True},
        default_factory=uuid.uuid4,
        **kwargs
    )

# Definição especial de campos --------------------------------
# noinspection PyPep8Naming
def FPKUuid7(**kwargs):
    # noinspection PyTypeChecker
    return Field(
        sa_type=UUID(),
        sa_column_kwargs={"server_default": func.uuid_v7()},
        default_factory=uuid.uuid7,
        primary_key=True,
        **kwargs
    )

# noinspection PyPep8Naming
def FKUuid7(**kwargs):
    # noinspection PyTypeChecker
    return Field(
        sa_type=UUID(),
        sa_column_kwargs={
            "server_default": func.uuid_v7(),
            "index": True
        },
        default_factory=uuid.uuid7,
        **kwargs
    )

# noinspection PyPep8Naming
def FChar(sz:int, **kwargs):
    # noinspection PyTypeChecker
    return Field(sa_type=String(sz), **kwargs)

# noinspection PyPep8Naming
def FTimestampHR(fsp:int=6, **kwargs):
    # noinspection PyTypeChecker
    return Field(
        sa_type=TIMESTAMP(fsp=fsp),
        sa_column_kwargs={"server_default": func.current_timestamp(6)},
        **kwargs
    )
