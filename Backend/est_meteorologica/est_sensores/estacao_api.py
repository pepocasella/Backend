from ninja import Router
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import List
from .models import Estacao
from .estacao_schemas import (
    EstacaoInput, 
    EstacaoUpdateInput, 
    EstacaoOutput, 
    EstacaoListOutput,
    EstacaoDeleteResponse
)

router = Router(tags=["Estações"])


@router.get("/", response=List[EstacaoListOutput])
def listar_estacoes(request):
    """Lista todas as estações meteorológicas"""
    estacoes = Estacao.objects.all().order_by('-criado_em')
    return estacoes


@router.get("/{estacao_id}", response=EstacaoOutput)
def obter_estacao(request, estacao_id: int):
    """Recupera uma estação específica pelo ID"""
    try:
        estacao = get_object_or_404(Estacao, id=estacao_id)
        return estacao
    except Http404:
        return {"error": "Estação não encontrada"}, 404


@router.post("/", response=EstacaoOutput)
def criar_estacao(request, dados: EstacaoInput):
    """Cria uma nova estação meteorológica"""
    try:
        # Validar se o usuário existe (se fornecido)
        if dados.criado_por:
            from est_accounts.models import User
            get_object_or_404(User, id=dados.criado_por)
        
        estacao = Estacao.objects.create(
            nome=dados.nome,
            localizacao=dados.localizacao,
            criado_por_id=dados.criado_por
        )
        return estacao
    except Exception as e:
        return {"error": f"Erro ao criar estação: {str(e)}"}, 400


@router.put("/{estacao_id}", response=EstacaoOutput)
def atualizar_estacao(request, estacao_id: int, dados: EstacaoUpdateInput):
    """Atualiza uma estação existente"""
    try:
        estacao = get_object_or_404(Estacao, id=estacao_id)
        
        # Atualizar apenas os campos fornecidos
        if dados.nome is not None:
            estacao.nome = dados.nome
        if dados.localizacao is not None:
            estacao.localizacao = dados.localizacao
            
        estacao.save()
        return estacao
    except Http404:
        return {"error": "Estação não encontrada"}, 404
    except Exception as e:
        return {"error": f"Erro ao atualizar estação: {str(e)}"}, 400


@router.patch("/{estacao_id}", response=EstacaoOutput)
def atualizar_estacao_parcial(request, estacao_id: int, dados: EstacaoUpdateInput):
    """Atualiza parcialmente uma estação existente"""
    try:
        estacao = get_object_or_404(Estacao, id=estacao_id)
        
        # Atualizar apenas os campos fornecidos
        if dados.nome is not None:
            estacao.nome = dados.nome
        if dados.localizacao is not None:
            estacao.localizacao = dados.localizacao
            
        estacao.save()
        return estacao
    except Http404:
        return {"error": "Estação não encontrada"}, 404
    except Exception as e:
        return {"error": f"Erro ao atualizar estação: {str(e)}"}, 400


@router.delete("/{estacao_id}", response=EstacaoDeleteResponse)
def deletar_estacao(request, estacao_id: int):
    """Deleta uma estação meteorológica"""
    try:
        estacao = get_object_or_404(Estacao, id=estacao_id)
        estacao_id_deleted = estacao.id
        estacao.delete()
        return {
            "message": f"Estação '{estacao.nome}' deletada com sucesso",
            "deleted_id": estacao_id_deleted
        }
    except Http404:
        return {"error": "Estação não encontrada"}, 404
    except Exception as e:
        return {"error": f"Erro ao deletar estação: {str(e)}"}, 400
