<template>
  <div class="estacao-form">
    <div class="form-header">
      <h3>{{ isEditing ? 'Editar Estação' : 'Nova Estação' }}</h3>
      <button @click="fecharFormulario" class="btn-close">×</button>
    </div>

    <form @submit.prevent="salvarEstacao" class="form">
      <div class="form-group">
        <label for="nome">Nome da Estação *</label>
        <input
          type="text"
          id="nome"
          v-model="formData.nome"
          :class="{ 'error': errors.nome }"
          placeholder="Digite o nome da estação"
          required
        />
        <span v-if="errors.nome" class="error-message">{{ errors.nome }}</span>
      </div>

      <div class="form-group">
        <label for="localizacao">Localização *</label>
        <input
          type="text"
          id="localizacao"
          v-model="formData.localizacao"
          :class="{ 'error': errors.localizacao }"
          placeholder="Digite a localização da estação"
          required
        />
        <span v-if="errors.localizacao" class="error-message">{{ errors.localizacao }}</span>
      </div>

      <div class="form-group">
        <label for="criado_por">ID do Usuário (opcional)</label>
        <input
          type="number"
          id="criado_por"
          v-model.number="formData.criado_por"
          placeholder="ID do usuário que criou a estação"
        />
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">
        <p>{{ isEditing ? 'Atualizando estação...' : 'Criando estação...' }}</p>
      </div>

      <!-- Error -->
      <div v-if="error" class="error">
        <p>{{ error }}</p>
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="success">
        <p>{{ successMessage }}</p>
      </div>

      <div class="form-actions">
        <button type="button" @click="fecharFormulario" class="btn btn-secondary">
          Cancelar
        </button>
        <button type="submit" :disabled="loading" class="btn btn-primary">
          {{ isEditing ? 'Atualizar' : 'Criar' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import EstacaoService from '../service/estacao_service.js'

export default {
  name: 'EstacaoForm',
  props: {
    estacao: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      formData: {
        nome: '',
        localizacao: '',
        criado_por: null
      },
      errors: {},
      loading: false,
      error: '',
      successMessage: ''
    }
  },
  computed: {
    isEditing() {
      return this.estacao && this.estacao.id
    }
  },
  watch: {
    estacao: {
      handler(newEstacao) {
        if (newEstacao) {
          this.formData = {
            nome: newEstacao.nome || '',
            localizacao: newEstacao.localizacao || '',
            criado_por: newEstacao.criado_por || null
          }
        } else {
          this.resetForm()
        }
      },
      immediate: true
    }
  },
  methods: {
    resetForm() {
      this.formData = {
        nome: '',
        localizacao: '',
        criado_por: null
      }
      this.errors = {}
      this.error = ''
      this.successMessage = ''
    },

    validateForm() {
      this.errors = {}
      let isValid = true

      if (!this.formData.nome.trim()) {
        this.errors.nome = 'Nome é obrigatório'
        isValid = false
      } else if (this.formData.nome.length > 100) {
        this.errors.nome = 'Nome deve ter no máximo 100 caracteres'
        isValid = false
      }

      if (!this.formData.localizacao.trim()) {
        this.errors.localizacao = 'Localização é obrigatória'
        isValid = false
      } else if (this.formData.localizacao.length > 255) {
        this.errors.localizacao = 'Localização deve ter no máximo 255 caracteres'
        isValid = false
      }

      return isValid
    },

    async salvarEstacao() {
      if (!this.validateForm()) {
        return
      }

      this.loading = true
      this.error = ''
      this.successMessage = ''

      try {
        const dados = {
          nome: this.formData.nome.trim(),
          localizacao: this.formData.localizacao.trim(),
          criado_por: this.formData.criado_por || null
        }

        if (this.isEditing) {
          await EstacaoService.atualizarEstacao(this.estacao.id, dados)
          this.successMessage = 'Estação atualizada com sucesso!'
        } else {
          await EstacaoService.criarEstacao(dados)
          this.successMessage = 'Estação criada com sucesso!'
        }

        // Emitir evento para atualizar a lista
        this.$emit('estacao-salva')
        
        // Fechar formulário após um breve delay para mostrar a mensagem de sucesso
        setTimeout(() => {
          this.fecharFormulario()
        }, 1500)

      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    fecharFormulario() {
      this.resetForm()
      this.$emit('fechar-formulario')
    }
  }
}
</script>

<style scoped>
.estacao-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  max-width: 500px;
  margin: 0 auto;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 20px 0 20px;
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 20px;
}

.form-header h3 {
  margin: 0;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: #333;
}

.form {
  padding: 0 20px 20px 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.form-group input.error {
  border-color: #dc3545;
}

.error-message {
  display: block;
  color: #dc3545;
  font-size: 12px;
  margin-top: 5px;
}

.loading, .error, .success {
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
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

.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
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
</style>
