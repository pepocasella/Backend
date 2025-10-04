<script setup>
import { ref, onMounted } from 'vue'
import EstacaoList from './components/EstacaoList.vue'
import EstacaoForm from './components/EstacaoForm.vue'
import LeituraFilters from './components/LeituraFilters.vue'
import LeituraTable from './components/LeituraTable.vue'
import LeituraService from './service/leitura_service.js'

// Estado da aplicação
const showForm = ref(false)
const estacaoEditando = ref(null)
const currentView = ref('estacoes') // 'estacoes' ou 'leituras'

// Estado para leituras
const leituras = ref([])
const loadingLeituras = ref(false)
const errorLeituras = ref('')
const filtrosAtivos = ref(null)

// Métodos para gerenciar o formulário
function abrirFormulario(estacao = null) {
  estacaoEditando.value = estacao
  showForm.value = true
}

function fecharFormulario() {
  showForm.value = false
  estacaoEditando.value = null
}

function onEstacaoSalva() {
  // O componente EstacaoList será atualizado automaticamente
  // através do evento emitido pelo EstacaoForm
}

// Métodos para leituras
async function aplicarFiltrosLeituras(filtros) {
  filtrosAtivos.value = filtros
  await buscarLeituras(filtros)
}

function limparFiltrosLeituras() {
  filtrosAtivos.value = null
  leituras.value = []
  errorLeituras.value = ''
}

async function buscarLeituras(filtros) {
  if (!filtros.estacaoId) return

  loadingLeituras.value = true
  errorLeituras.value = ''

  try {
    leituras.value = await LeituraService.listarLeituras(
      filtros.estacaoId,
      filtros.dataInicio,
      filtros.dataFim
    )
  } catch (error) {
    errorLeituras.value = error.message
    leituras.value = []
  } finally {
    loadingLeituras.value = false
  }
}

async function recarregarLeituras() {
  if (filtrosAtivos.value) {
    await buscarLeituras(filtrosAtivos.value)
  }
}
</script>

<template>
  <div class="app">
    <!-- Header -->
    <header class="app-header">
      <h1>Sistema de Estação Meteorológica</h1>
      <nav class="nav-tabs">
        <button 
          @click="currentView = 'estacoes'" 
          :class="{ active: currentView === 'estacoes' }"
          class="nav-tab"
        >
          Estações
        </button>
        <button 
          @click="currentView = 'leituras'" 
          :class="{ active: currentView === 'leituras' }"
          class="nav-tab"
        >
          Leituras
        </button>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <!-- View de Estações -->
      <div v-if="currentView === 'estacoes'">
        <EstacaoList 
          @abrir-formulario="abrirFormulario"
        />
      </div>

      <!-- View de Leituras -->
      <div v-if="currentView === 'leituras'" class="leituras-view">
        <LeituraFilters 
          @aplicar-filtros="aplicarFiltrosLeituras"
          @limpar-filtros="limparFiltrosLeituras"
        />
        
        <LeituraTable 
          :leituras="leituras"
          :loading="loadingLeituras"
          :error="errorLeituras"
          @recarregar="recarregarLeituras"
        />
      </div>
    </main>

    <!-- Modal do Formulário -->
    <div v-if="showForm" class="modal-overlay" @click="fecharFormulario">
      <div class="modal-content" @click.stop>
        <EstacaoForm 
          :estacao="estacaoEditando"
          @fechar-formulario="fecharFormulario"
          @estacao-salva="onEstacaoSalva"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.app-header {
  background: white;
  border-bottom: 1px solid #dee2e6;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-header h1 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 24px;
}

.nav-tabs {
  display: flex;
  gap: 0;
}

.nav-tab {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  color: #6c757d;
  font-weight: 500;
}

.nav-tab:hover {
  color: #007bff;
  background-color: #f8f9fa;
}

.nav-tab.active {
  color: #007bff;
  border-bottom-color: #007bff;
  background-color: #f8f9fa;
}

.app-main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.leituras-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.modal-content {
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}
</style>