from ninja import NinjaAPI
from .schemas import DadosEstacaoInput
from est_sensores.api import router as sensores_router


api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"


@api.post("/dados/")
def receber_dados(request, dados: DadosEstacaoInput):
    print(">>> Dados recebidos da estação:", dados.payload)
    return {"status": "ok", "mensagem": "Dados recebidos com sucesso!"}


api.add_router("/sensores/", sensores_router)