const API_BASE_URL = 'http://localhost:8000/api'

class LeituraService {
  async listarLeituras(estacaoId, dataInicio = null, dataFim = null) {
    try {
      let url = `${API_BASE_URL}/sensores/estacoes/${estacaoId}/leituras/`
      
      // Adicionar parâmetros de data se fornecidos
      const params = new URLSearchParams()
      if (dataInicio) {
        params.append('data_inicio', dataInicio)
      }
      if (dataFim) {
        params.append('data_fim', dataFim)
      }
      
      if (params.toString()) {
        url += `?${params.toString()}`
      }

      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Erro ao listar leituras:', error)
      throw error
    }
  }

  async listarEstacoes() {
    try {
      const response = await fetch(`${API_BASE_URL}/estacoes/`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Erro ao listar estações:', error)
      throw error
    }
  }

  formatarDataParaAPI(data) {
    // Converte data do formato brasileiro para ISO
    if (!data) return null
    const [dia, mes, ano] = data.split('/')
    return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`
  }

  formatarDataParaExibicao(dataISO) {
    // Converte data ISO para formato brasileiro
    if (!dataISO) return ''
    const data = new Date(dataISO)
    return data.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }
}

export default new LeituraService()
