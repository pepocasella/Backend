# CRUD Completo para Estações Meteorológicas

Este documento contém o código completo para um CRUD de estações meteorológicas usando Django Ninja e Vue.js.

## 📁 Estrutura dos Arquivos

### Backend (Django Ninja)

#### 1. Schemas Pydantic
**Arquivo:** `Backend/est_meteorologica/est_sensores/estacao_schemas.py`
- `EstacaoInput`: Schema para criação de estações
- `EstacaoUpdateInput`: Schema para atualização de estações
- `EstacaoOutput`: Schema de resposta completa
- `EstacaoListOutput`: Schema para listagem
- `EstacaoDeleteResponse`: Schema para resposta de exclusão

#### 2. Endpoints da API
**Arquivo:** `Backend/est_meteorologica/est_sensores/estacao_api.py`
- `GET /estacoes/` - Listar todas as estações
- `GET /estacoes/{id}` - Obter estação específica
- `POST /estacoes/` - Criar nova estação
- `PUT /estacoes/{id}` - Atualizar estação (completa)
- `PATCH /estacoes/{id}` - Atualizar estação (parcial)
- `DELETE /estacoes/{id}` - Deletar estação

#### 3. Configuração da API
**Arquivo:** `Backend/est_meteorologica/est_meteorologica/api.py`
- Adicionado router das estações: `api.add_router("/estacoes/", estacao_router)`

### Frontend (Vue.js)

#### 1. Serviço de API
**Arquivo:** `Frontend/est_meteorologica/src/service/estacao_service.js`
- Métodos para comunicação com a API Django
- Tratamento de erros
- Uso de fetch API

#### 2. Componente de Listagem
**Arquivo:** `Frontend/est_meteorologica/src/components/EstacaoList.vue`
- Tabela responsiva com todas as estações
- Botões de ação (Editar/Deletar)
- Modal de confirmação para exclusão
- Estados de loading, erro e sucesso

#### 3. Componente de Formulário
**Arquivo:** `Frontend/est_meteorologica/src/components/EstacaoForm.vue`
- Formulário para criar/editar estações
- Validação de campos
- Tratamento de erros
- Estados de loading

#### 4. Aplicação Principal
**Arquivo:** `Frontend/est_meteorologica/src/App.vue`
- Integração de todos os componentes
- Navegação por abas
- Modal para formulário

## 🚀 Como Usar

### 1. Backend (Django)

1. **Instalar dependências:**
```bash
cd Backend/est_meteorologica
pip install -r requirements.txt
```

2. **Executar migrações:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Iniciar servidor:**
```bash
python manage.py runserver
```

### 2. Frontend (Vue.js)

1. **Instalar dependências:**
```bash
cd Frontend/est_meteorologica
npm install
```

2. **Iniciar servidor de desenvolvimento:**
```bash
npm run dev
```

## 📋 Endpoints da API

### Listar Estações
```http
GET http://localhost:8000/api/estacoes/
```

### Obter Estação
```http
GET http://localhost:8000/api/estacoes/{id}
```

### Criar Estação
```http
POST http://localhost:8000/api/estacoes/
Content-Type: application/json

{
  "nome": "Estação Central",
  "localizacao": "São Paulo, SP",
  "criado_por": 1
}
```

### Atualizar Estação
```http
PUT http://localhost:8000/api/estacoes/{id}
Content-Type: application/json

{
  "nome": "Estação Central Atualizada",
  "localizacao": "São Paulo, SP - Centro"
}
```

### Deletar Estação
```http
DELETE http://localhost:8000/api/estacoes/{id}
```

## 🎨 Funcionalidades do Frontend

### Lista de Estações
- ✅ Tabela responsiva com todas as estações
- ✅ Botão para criar nova estação
- ✅ Botões de editar e deletar
- ✅ Modal de confirmação para exclusão
- ✅ Estados de loading e erro
- ✅ Mensagens de sucesso

### Formulário de Estação
- ✅ Campos: Nome, Localização, ID do Usuário (opcional)
- ✅ Validação de campos obrigatórios
- ✅ Validação de tamanho máximo
- ✅ Modo criação e edição
- ✅ Tratamento de erros da API
- ✅ Estados de loading

### Interface
- ✅ Design moderno e responsivo
- ✅ Navegação por abas
- ✅ Modal para formulário
- ✅ Mensagens de feedback
- ✅ Animações suaves

## 🔧 Configurações

### CORS
O Django está configurado para aceitar requisições do frontend Vue.js:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

### URL Base da API
No frontend, a URL base está configurada como:
```javascript
const API_BASE_URL = 'http://localhost:8000/api'
```

## 🐛 Tratamento de Erros

### Backend
- Validação de dados com Pydantic
- Tratamento de exceções HTTP
- Mensagens de erro descritivas
- Status codes apropriados

### Frontend
- Try/catch em todas as chamadas da API
- Exibição de mensagens de erro
- Estados de loading
- Validação de formulário

## 📱 Responsividade

O frontend foi desenvolvido com foco em responsividade:
- Tabela com scroll horizontal em telas pequenas
- Modal responsivo
- Botões adaptáveis
- Layout flexível

## 🎯 Próximos Passos

1. **Autenticação:** Implementar sistema de login
2. **Permissões:** Controle de acesso baseado em usuário
3. **Paginação:** Implementar paginação na listagem
4. **Filtros:** Adicionar filtros de busca
5. **Exportação:** Exportar dados para CSV/Excel
6. **Testes:** Implementar testes unitários e de integração

## 📝 Notas Técnicas

- **Backend:** Django 5.2 + Django Ninja + SQLite
- **Frontend:** Vue.js 3 + Composition API
- **Estilo:** CSS puro com design system
- **Comunicação:** Fetch API (pode ser substituído por Axios)
- **Validação:** Pydantic no backend, validação manual no frontend
