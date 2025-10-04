from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Estacao, Sensor
from .schemas import LeituraBatchInput, LeituraOutput


router = Router(tags=["Sensores"])

@router.post("{estacao_id}/leituras/")
def receber_leituras(request, estacao_id: str, dados: LeituraBatchInput):
    estacao = get_object_or_404(Estacao, nome=estacao_id)
    
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
def listar_leituras(request, estacao_id: int, data_inicio: str = None, data_fim: str = None):
    """
    Lista leituras de uma estação específica com filtros opcionais de data
    
    Args:
        estacao_id: ID da estação
        data_inicio: Data de início no formato YYYY-MM-DD (opcional)
        data_fim: Data de fim no formato YYYY-MM-DD (opcional)
    """
    from datetime import datetime, time
    
    estacao = get_object_or_404(Estacao, id=estacao_id)
    leituras = Sensor.objects.filter(estacao=estacao)
    
    # Aplicar filtros de data se fornecidos
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            leituras = leituras.filter(timestamp__date__gte=data_inicio_obj)
        except ValueError:
            return {"error": "Formato de data_inicio inválido. Use YYYY-MM-DD"}, 400
    
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            # Incluir todo o dia da data_fim
            data_fim_completa = datetime.combine(data_fim_obj, time.max)
            leituras = leituras.filter(timestamp__lte=data_fim_completa)
        except ValueError:
            return {"error": "Formato de data_fim inválido. Use YYYY-MM-DD"}, 400
    
    # Ordenar por timestamp decrescente e limitar a 1000 registros
    leituras = leituras.order_by("-timestamp")[:1000]
    return leituras
