from ninja import Schema
from typing import List
from datetime import datetime


class LeituraInput(Schema):
    sensor: str
    medida: str
    valor: float
    unidade: str


class LeituraBatchInput(Schema):
    leituras: List[LeituraInput]


class LeituraOutput(Schema):
    id: int
    sensor: str
    medida: str
    valor: float
    unidade: str
    timestamp: datetime
