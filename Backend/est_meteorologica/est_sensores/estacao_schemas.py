from ninja import Schema
from typing import Optional
from datetime import datetime


class EstacaoInput(Schema):
    nome: str
    localizacao: str
    criado_por: Optional[int] = None


class EstacaoUpdateInput(Schema):
    nome: Optional[str] = None
    localizacao: Optional[str] = None


class EstacaoOutput(Schema):
    id: int
    nome: str
    localizacao: str
    criado_por: Optional[int] = None
    criado_em: datetime
    modificado_em: datetime


class EstacaoListOutput(Schema):
    id: int
    nome: str
    localizacao: str
    criado_em: datetime


class EstacaoDeleteResponse(Schema):
    message: str
    deleted_id: int
