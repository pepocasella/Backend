const API_BASE_URL = 'http://localhost:8000/api'

class EstacaoService {
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

  async obterEstacao(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/estacoes/${id}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Erro ao obter estação:', error)
      throw error
    }
  }

  async criarEstacao(dados) {
    try {
      const response = await fetch(`${API_BASE_URL}/estacoes/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados)
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Erro ao criar estação:', error)
      throw error
    }
  }

  async atualizarEstacao(id, dados) {
    try {
      const response = await fetch(`${API_BASE_URL}/estacoes/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados)
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Erro ao atualizar estação:', error)
      throw error
    }
  }

  async deletarEstacao(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/estacoes/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Erro ao deletar estação:', error)
      throw error
    }
  }
}

export default new EstacaoService()
