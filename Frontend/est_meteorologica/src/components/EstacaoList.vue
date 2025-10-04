<template>
  <div class="estacao-list">
    <div class="header">
      <h2>Estações Meteorológicas</h2>
      <button @click="abrirFormulario()" class="btn btn-primary">
        <i class="icon">+</i> Nova Estação
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <p>Carregando estações...</p>
    </div>

    <!-- Error -->
    <div v-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="carregarEstacoes" class="btn btn-secondary">Tentar novamente</button>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="success">
      <p>{{ successMessage }}</p>
      <button @click="successMessage = ''" class="btn-close">×</button>
    </div>

    <!-- Table -->
    <div v-if="!loading && !error" class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Localização</th>
            <th>Data de Criação</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="estacao in estacoes" :key="estacao.id">
            <td>{{ estacao.id }}</td>
            <td>{{ estacao.nome }}</td>
            <td>{{ estacao.localizacao }}</td>
            <td>{{ formatarData(estacao.criado_em) }}</td>
            <td class="actions">
              <button @click="editarEstacao(estacao)" class="btn btn-sm btn-secondary">
                Editar
              </button>
              <button @click="deletarEstacao(estacao.id)" class="btn btn-sm btn-danger">
                Deletar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="estacoes.length === 0" class="empty">
        <p>Nenhuma estação encontrada.</p>
      </div>
    </div>

    <!-- Modal de Confirmação -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="fecharModal">
      <div class="modal" @click.stop>
        <h3>Confirmar Exclusão</h3>
        <p>Tem certeza que deseja deletar esta estação?</p>
        <div class="modal-actions">
          <button @click="fecharModal" class="btn btn-secondary">Cancelar</button>
          <button @click="confirmarDelecao" class="btn btn-danger">Deletar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EstacaoService from '../service/estacao_service.js'

export default {
  name: 'EstacaoList',
  data() {
    return {
      estacoes: [],
      loading: false,
      error: '',
      successMessage: '',
      showDeleteModal: false,
      estacaoParaDeletar: null
    }
  },
  mounted() {
    this.carregarEstacoes()
  },
  methods: {
    async carregarEstacoes() {
      this.loading = true
      this.error = ''
      try {
        this.estacoes = await EstacaoService.listarEstacoes()
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    abrirFormulario(estacao = null) {
      this.$emit('abrir-formulario', estacao)
    },

    editarEstacao(estacao) {
      this.abrirFormulario(estacao)
    },

    deletarEstacao(id) {
      this.estacaoParaDeletar = id
      this.showDeleteModal = true
    },

    async confirmarDelecao() {
      if (!this.estacaoParaDeletar) return

      try {
        await EstacaoService.deletarEstacao(this.estacaoParaDeletar)
        this.successMessage = 'Estação deletada com sucesso!'
        this.carregarEstacoes()
      } catch (error) {
        this.error = error.message
      } finally {
        this.fecharModal()
      }
    },

    fecharModal() {
      this.showDeleteModal = false
      this.estacaoParaDeletar = null
    },

    formatarData(data) {
      return new Date(data).toLocaleString('pt-BR')
    }
  }
}
</script>

<style scoped>
.estacao-list {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  color: #333;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
  margin-right: 4px;
}

.loading, .error, .success {
  padding: 20px;
  text-align: center;
  border-radius: 4px;
  margin-bottom: 20px;
}

.loading {
  background-color: #f8f9fa;
  color: #6c757d;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #155724;
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table th,
.table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #495057;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}

.actions {
  white-space: nowrap;
}

.empty {
  text-align: center;
  padding: 40px;
  color: #6c757d;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.modal h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.modal p {
  margin: 0 0 20px 0;
  color: #666;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.icon {
  margin-right: 4px;
}
</style>
