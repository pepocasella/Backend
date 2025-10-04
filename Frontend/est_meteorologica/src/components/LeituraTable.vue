<template>
  <div class="leitura-table">
    <div class="table-header">
      <h3>Leituras dos Sensores</h3>
      <div v-if="leituras.length > 0" class="table-info">
        <span>{{ leiturasFiltradas.length }} de {{ leituras.length }} leitura(s)</span>
      </div>
    </div>

    <!-- Controles de Busca e Ordenação -->
    <div v-if="leituras.length > 0" class="table-controls">
      <div class="search-container">
        <div class="search-input-wrapper">
          <i class="search-icon">🔍</i>
          <input
            type="text"
            v-model="searchTerm"
            placeholder="Buscar em todas as colunas..."
            class="search-input"
          />
          <button 
            v-if="searchTerm" 
            @click="clearSearch" 
            class="clear-search"
            title="Limpar busca"
          >
            ×
          </button>
        </div>
      </div>
      
      <div class="sort-controls">
        <label for="sort-select">Ordenar por:</label>
        <select id="sort-select" v-model="sortField" class="sort-select">
          <option value="">Selecionar coluna</option>
          <option value="id">ID</option>
          <option value="sensor">Sensor</option>
          <option value="medida">Medida</option>
          <option value="valor">Valor</option>
          <option value="unidade">Unidade</option>
          <option value="timestamp">Data/Hora</option>
        </select>
        
        <button 
          @click="toggleSortOrder" 
          class="sort-order-btn"
          :class="{ 'desc': sortOrder === 'desc' }"
          :disabled="!sortField"
          title="Alternar ordem"
        >
          {{ sortOrder === 'asc' ? '↑' : '↓' }}
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <p>Carregando leituras...</p>
    </div>

    <!-- Error -->
    <div v-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="$emit('recarregar')" class="btn btn-secondary">Tentar novamente</button>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && !error && leituras.length === 0" class="empty">
      <div class="empty-icon">📊</div>
      <h4>Nenhuma leitura encontrada</h4>
      <p>Selecione uma estação e aplique os filtros para ver as leituras.</p>
    </div>

    <!-- Table -->
    <div v-if="!loading && !error && leituras.length > 0" class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th 
              @click="sort('id')" 
              :class="{ 'sortable': true, 'sorted': sortField === 'id' }"
              class="sortable-header"
            >
              ID
              <span v-if="sortField === 'id'" class="sort-indicator">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th 
              @click="sort('sensor')" 
              :class="{ 'sortable': true, 'sorted': sortField === 'sensor' }"
              class="sortable-header"
            >
              Sensor
              <span v-if="sortField === 'sensor'" class="sort-indicator">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th 
              @click="sort('medida')" 
              :class="{ 'sortable': true, 'sorted': sortField === 'medida' }"
              class="sortable-header"
            >
              Medida
              <span v-if="sortField === 'medida'" class="sort-indicator">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th 
              @click="sort('valor')" 
              :class="{ 'sortable': true, 'sorted': sortField === 'valor' }"
              class="sortable-header"
            >
              Valor
              <span v-if="sortField === 'valor'" class="sort-indicator">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th 
              @click="sort('unidade')" 
              :class="{ 'sortable': true, 'sorted': sortField === 'unidade' }"
              class="sortable-header"
            >
              Unidade
              <span v-if="sortField === 'unidade'" class="sort-indicator">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th 
              @click="sort('timestamp')" 
              :class="{ 'sortable': true, 'sorted': sortField === 'timestamp' }"
              class="sortable-header"
            >
              Data/Hora
              <span v-if="sortField === 'timestamp'" class="sort-indicator">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="leitura in leiturasFiltradas" :key="leitura.id">
            <td>{{ leitura.id }}</td>
            <td>
              <span class="sensor-badge" :class="getSensorClass(leitura.sensor)">
                {{ leitura.sensor }}
              </span>
            </td>
            <td>{{ leitura.medida }}</td>
            <td class="valor-cell">
              <span class="valor" :class="getValorClass(leitura.valor, leitura.medida)">
                {{ formatarValor(leitura.valor) }}
              </span>
            </td>
            <td>{{ leitura.unidade }}</td>
            <td>{{ formatarData(leitura.timestamp) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Resumo das Leituras -->
    <div v-if="!loading && !error && leituras.length > 0" class="resumo">
      <h4>Resumo das Leituras</h4>
      <div class="resumo-grid">
        <div class="resumo-item">
          <span class="label">Total de Leituras:</span>
          <span class="value">{{ leiturasFiltradas.length }} de {{ leituras.length }}</span>
        </div>
        <div class="resumo-item">
          <span class="label">Sensores Únicos:</span>
          <span class="value">{{ sensoresUnicosFiltrados }}</span>
        </div>
        <div class="resumo-item">
          <span class="label">Período:</span>
          <span class="value">{{ periodoLeiturasFiltradas }}</span>
        </div>
        <div v-if="searchTerm" class="resumo-item">
          <span class="label">Filtro Ativo:</span>
          <span class="value">"{{ searchTerm }}"</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LeituraService from '../service/leitura_service.js'

export default {
  name: 'LeituraTable',
  props: {
    leituras: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      searchTerm: '',
      sortField: '',
      sortOrder: 'asc'
    }
  },
  computed: {
    leiturasFiltradas() {
      let filtered = [...this.leituras]
      
      // Aplicar busca global
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase()
        filtered = filtered.filter(leitura => {
          return (
            leitura.id.toString().includes(term) ||
            leitura.sensor.toLowerCase().includes(term) ||
            leitura.medida.toLowerCase().includes(term) ||
            leitura.valor.toString().includes(term) ||
            leitura.unidade.toLowerCase().includes(term) ||
            this.formatarData(leitura.timestamp).toLowerCase().includes(term)
          )
        })
      }
      
      // Aplicar ordenação
      if (this.sortField) {
        filtered.sort((a, b) => {
          let aVal = a[this.sortField]
          let bVal = b[this.sortField]
          
          // Tratamento especial para diferentes tipos de dados
          if (this.sortField === 'valor') {
            aVal = parseFloat(aVal) || 0
            bVal = parseFloat(bVal) || 0
          } else if (this.sortField === 'timestamp') {
            aVal = new Date(aVal)
            bVal = new Date(bVal)
          } else if (this.sortField === 'id') {
            aVal = parseInt(aVal) || 0
            bVal = parseInt(bVal) || 0
          } else {
            aVal = String(aVal).toLowerCase()
            bVal = String(bVal).toLowerCase()
          }
          
          if (aVal < bVal) return this.sortOrder === 'asc' ? -1 : 1
          if (aVal > bVal) return this.sortOrder === 'asc' ? 1 : -1
          return 0
        })
      }
      
      return filtered
    },
    sensoresUnicosFiltrados() {
      const sensores = new Set(this.leiturasFiltradas.map(l => l.sensor))
      return sensores.size
    },
    periodoLeiturasFiltradas() {
      if (this.leiturasFiltradas.length === 0) return 'N/A'
      
      const timestamps = this.leiturasFiltradas.map(l => new Date(l.timestamp))
      const maisAntiga = new Date(Math.min(...timestamps))
      const maisRecente = new Date(Math.max(...timestamps))
      
      return `${this.formatarData(maisAntiga)} - ${this.formatarData(maisRecente)}`
    }
  },
  methods: {
    formatarData(dataISO) {
      return LeituraService.formatarDataParaExibicao(dataISO)
    },

    formatarValor(valor) {
      return typeof valor === 'number' ? valor.toFixed(2) : valor
    },

    getSensorClass(sensor) {
      const classes = {
        'DHT11': 'sensor-dht11',
        'LM35': 'sensor-lm35',
        'BMP280': 'sensor-bmp280',
        'default': 'sensor-default'
      }
      return classes[sensor] || classes.default
    },

    getValorClass(valor, medida) {
      if (medida.toLowerCase().includes('temperatura')) {
        if (valor > 30) return 'valor-alto'
        if (valor < 10) return 'valor-baixo'
        return 'valor-normal'
      }
      if (medida.toLowerCase().includes('umidade')) {
        if (valor > 80) return 'valor-alto'
        if (valor < 30) return 'valor-baixo'
        return 'valor-normal'
      }
      return 'valor-normal'
    },

    // Métodos para ordenação
    sort(field) {
      if (this.sortField === field) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortOrder = 'asc'
      }
    },

    toggleSortOrder() {
      if (this.sortField) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      }
    },

    // Métodos para busca
    clearSearch() {
      this.searchTerm = ''
    }
  }
}
</script>

<style scoped>
.leitura-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
}

.table-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.table-info {
  color: #6c757d;
  font-size: 14px;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  gap: 20px;
}

.search-container {
  flex: 1;
  max-width: 400px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: #6c757d;
  font-size: 16px;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 40px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.clear-search {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  font-size: 18px;
  padding: 4px;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.clear-search:hover {
  background-color: #e9ecef;
  color: #495057;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.sort-controls label {
  color: #495057;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.sort-select {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.sort-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.sort-order-btn {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  color: #495057;
  transition: all 0.2s;
  min-width: 40px;
}

.sort-order-btn:hover:not(:disabled) {
  background-color: #f8f9fa;
  border-color: #007bff;
}

.sort-order-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sort-order-btn.desc {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.sortable-header {
  cursor: pointer;
  user-select: none;
  position: relative;
  transition: background-color 0.2s;
}

.sortable-header:hover {
  background-color: #e9ecef;
}

.sortable-header.sorted {
  background-color: #e3f2fd;
  color: #1976d2;
}

.sort-indicator {
  margin-left: 8px;
  font-weight: bold;
  color: #007bff;
}

.loading, .error, .empty {
  padding: 40px;
  text-align: center;
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

.empty {
  color: #6c757d;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty h4 {
  margin: 0 0 8px 0;
  color: #495057;
}

.empty p {
  margin: 0;
  font-size: 14px;
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
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
  position: sticky;
  top: 0;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}

.sensor-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.sensor-dht11 {
  background-color: #e3f2fd;
  color: #1976d2;
}

.sensor-lm35 {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.sensor-bmp280 {
  background-color: #e8f5e8;
  color: #388e3c;
}

.sensor-default {
  background-color: #f5f5f5;
  color: #616161;
}

.valor-cell {
  font-weight: 500;
}

.valor {
  padding: 2px 6px;
  border-radius: 4px;
}

.valor-normal {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.valor-alto {
  background-color: #ffebee;
  color: #c62828;
}

.valor-baixo {
  background-color: #e3f2fd;
  color: #1565c0;
}

.resumo {
  padding: 20px;
  border-top: 1px solid #dee2e6;
  background-color: #f8f9fa;
}

.resumo h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
}

.resumo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.resumo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: white;
  border-radius: 4px;
  border: 1px solid #dee2e6;
}

.resumo-item .label {
  color: #6c757d;
  font-size: 14px;
}

.resumo-item .value {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

/* Responsividade */
@media (max-width: 768px) {
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .table-controls {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .search-container {
    max-width: none;
  }
  
  .sort-controls {
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .sort-controls label {
    flex: 1;
    min-width: 100px;
  }
  
  .sort-select {
    flex: 1;
    min-width: 120px;
  }
  
  .resumo-grid {
    grid-template-columns: 1fr;
  }
  
  .table th,
  .table td {
    padding: 8px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .table-controls {
    padding: 15px;
  }
  
  .search-input {
    padding: 8px 35px 8px 35px;
    font-size: 16px; /* Evita zoom no iOS */
  }
  
  .sort-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .sort-controls label {
    margin-bottom: 5px;
  }
  
  .sort-select,
  .sort-order-btn {
    width: 100%;
  }
}
</style>
