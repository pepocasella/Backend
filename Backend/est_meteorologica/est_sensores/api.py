from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Estacao, Sensor
from .schemas import LeituraBatchInput, LeituraOutput


router = Router(tags=["Sensores"])

@router.post("{estacao_id}/leituras/")
def receber_leituras(request, estacao_id: str, dados: LeituraBatchInput):
    estacao = get_object_or_404(Estacao, identificador=estacao_id)
    
    sensores = [
        Sensor(
            estacao=estacao,
            sensor=leitura.sensor,
            medida=leitura.medida,
            valor=leitura.valor,
            unidade=leitura.unidade,
        )
        for leitura in dados.leituras
    ]
    Sensor.objects.bulk_create(sensores)
    return {"status": "ok", "mensagem": f"{len(sensores)} leituras salvas."}



@router.get("/estacoes/{estacao_id}/leituras/", response=list[LeituraOutput])
def listar_leituras(request, estacao_id: int):
    estacao = get_object_or_404(Estacao, id=estacao_id)
    leituras = Sensor.objects.filter(estacao=estacao).order_by("-timestamp")[:100]
    return leituras
