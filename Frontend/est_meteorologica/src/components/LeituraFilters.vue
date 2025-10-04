<template>
  <div class="leitura-filters">
    <div class="filters-header">
      <h3>Filtros de Leituras</h3>
    </div>

    <form @submit.prevent="aplicarFiltros" class="filters-form">
      <div class="form-row">
        <div class="form-group">
          <label for="estacao">Estação Meteorológica *</label>
          <select 
            id="estacao" 
            v-model="filters.estacaoId" 
            :class="{ 'error': errors.estacaoId }"
            required
          >
            <option value="">Selecione uma estação</option>
            <option 
              v-for="estacao in estacoes" 
              :key="estacao.id" 
              :value="estacao.id"
            >
              {{ estacao.nome }} - {{ estacao.localizacao }}
            </option>
          </select>
          <span v-if="errors.estacaoId" class="error-message">{{ errors.estacaoId }}</span>
        </div>

        <div class="form-group">
          <label for="dataInicio">Data Início</label>
          <input
            type="date"
            id="dataInicio"
            v-model="filters.dataInicio"
            :max="filters.dataFim || ''"
          />
        </div>

        <div class="form-group">
          <label for="dataFim">Data Fim</label>
          <input
            type="date"
            id="dataFim"
            v-model="filters.dataFim"
            :min="filters.dataInicio || ''"
          />
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="loading" class="btn btn-primary">
          <i class="icon">🔍</i> Buscar Leituras
        </button>
        <button type="button" @click="limparFiltros" class="btn btn-secondary">
          <i class="icon">🗑️</i> Limpar
        </button>
      </div>
    </form>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <p>Carregando estações...</p>
    </div>

    <!-- Error -->
    <div v-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="carregarEstacoes" class="btn btn-sm btn-secondary">Tentar novamente</button>
    </div>
  </div>
</template>

<script>
import LeituraService from '../service/leitura_service.js'

export default {
  name: 'LeituraFilters',
  data() {
    return {
      estacoes: [],
      filters: {
        estacaoId: '',
        dataInicio: '',
        dataFim: ''
      },
      errors: {},
      loading: false,
      error: ''
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
        this.estacoes = await LeituraService.listarEstacoes()
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    validateFilters() {
      this.errors = {}
      let isValid = true

      if (!this.filters.estacaoId) {
        this.errors.estacaoId = 'Selecione uma estação'
        isValid = false
      }

      if (this.filters.dataInicio && this.filters.dataFim) {
        const dataInicio = new Date(this.filters.dataInicio)
        const dataFim = new Date(this.filters.dataFim)
        
        if (dataInicio > dataFim) {
          this.errors.dataFim = 'Data fim deve ser maior que data início'
          isValid = false
        }
      }

      return isValid
    },

    async aplicarFiltros() {
      if (!this.validateFilters()) {
        return
      }

      const filtros = {
        estacaoId: this.filters.estacaoId,
        dataInicio: this.filters.dataInicio || null,
        dataFim: this.filters.dataFim || null
      }

      this.$emit('aplicar-filtros', filtros)
    },

    limparFiltros() {
      this.filters = {
        estacaoId: '',
        dataInicio: '',
        dataFim: ''
      }
      this.errors = {}
      this.$emit('limpar-filtros')
    }
  }
}
</script>

<style scoped>
.leitura-filters {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.filters-header {
  padding: 20px 20px 0 20px;
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 20px;
}

.filters-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.filters-form {
  padding: 0 20px 20px 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group select,
.form-group input {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group select:focus,
.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.form-group select.error,
.form-group input.error {
  border-color: #dc3545;
}

.error-message {
  display: block;
  color: #dc3545;
  font-size: 12px;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.loading, .error {
  padding: 20px;
  text-align: center;
  border-radius: 4px;
  margin: 20px;
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

.icon {
  font-size: 14px;
}

/* Responsividade */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    justify-content: center;
  }
}
</style>
