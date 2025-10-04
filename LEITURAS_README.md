# 📊 Sistema de Leituras de Sensores

Esta funcionalidade permite visualizar e filtrar as leituras dos sensores das estações meteorológicas por período de tempo.

## 🎯 Funcionalidades Implementadas

### ✅ **Filtros Avançados**
- **Seleção de Estação**: Dropdown com todas as estações disponíveis
- **Filtro por Data**: Data início e data fim opcionais
- **Validação**: Campos obrigatórios e validação de datas
- **Interface Responsiva**: Layout adaptável para mobile

### ✅ **Tabela de Leituras**
- **Visualização Completa**: ID, Sensor, Medida, Valor, Unidade, Data/Hora
- **Badges Coloridos**: Identificação visual por tipo de sensor
- **Valores Destacados**: Cores diferentes para valores altos/baixos/normais
- **Resumo Estatístico**: Total de leituras, sensores únicos, período

### ✅ **API Backend Melhorada**
- **Filtros de Data**: Suporte a `data_inicio` e `data_fim`
- **Validação**: Tratamento de erros de formato de data
- **Performance**: Limite de 1000 registros por consulta
- **Documentação**: Parâmetros claramente documentados

## 📁 Arquivos Criados/Modificados

### Frontend
1. **`src/service/leitura_service.js`** - Serviço para comunicação com API
2. **`src/components/LeituraFilters.vue`** - Componente de filtros
3. **`src/components/LeituraTable.vue`** - Tabela de leituras
4. **`src/App.vue`** - Integração da página de leituras

### Backend
1. **`est_sensores/api.py`** - Endpoint melhorado com filtros de data

## 🚀 Como Usar

### 1. **Acessar a Página**
- Clique na aba "Leituras" no menu principal
- A página carregará automaticamente as estações disponíveis

### 2. **Aplicar Filtros**
1. **Selecione uma Estação** (obrigatório)
2. **Defina Data Início** (opcional)
3. **Defina Data Fim** (opcional)
4. **Clique em "Buscar Leituras"**

### 3. **Visualizar Resultados**
- Tabela com todas as leituras encontradas
- Resumo estatístico na parte inferior
- Botão para recarregar em caso de erro

## 🔧 API Endpoints

### Listar Leituras com Filtros
```http
GET /api/sensores/estacoes/{estacao_id}/leituras/
```

**Parâmetros de Query:**
- `data_inicio` (opcional): Data no formato YYYY-MM-DD
- `data_fim` (opcional): Data no formato YYYY-MM-DD

**Exemplo:**
```http
GET /api/sensores/estacoes/1/leituras/?data_inicio=2024-01-01&data_fim=2024-01-31
```

**Resposta:**
```json
[
  {
    "id": 1,
    "sensor": "DHT11",
    "medida": "Temperatura",
    "valor": 25.5,
    "unidade": "°C",
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

## 🎨 Interface do Usuário

### **Filtros**
- **Layout em Grid**: 3 colunas responsivas
- **Validação Visual**: Campos com erro destacados em vermelho
- **Botões de Ação**: Buscar e Limpar filtros
- **Estados**: Loading, erro e sucesso

### **Tabela de Leituras**
- **Cabeçalho Fixo**: Scroll vertical mantém cabeçalho visível
- **Badges de Sensor**: Cores diferentes por tipo (DHT11, LM35, BMP280)
- **Valores Coloridos**: 
  - 🟢 Verde: Valores normais
  - 🔴 Vermelho: Valores altos
  - 🔵 Azul: Valores baixos
- **Hover Effect**: Linhas destacadas ao passar o mouse

### **Resumo Estatístico**
- **Total de Leituras**: Quantidade encontrada
- **Sensores Únicos**: Número de tipos de sensores
- **Período**: Data da primeira à última leitura

## 📱 Responsividade

### **Desktop (> 768px)**
- Filtros em 3 colunas
- Tabela completa
- Resumo em grid horizontal

### **Mobile (< 768px)**
- Filtros em coluna única
- Tabela com scroll horizontal
- Resumo em coluna única
- Botões empilhados

## 🔍 Tipos de Sensores Suportados

### **DHT11** 🔵
- Temperatura e Umidade
- Badge azul
- Valores: 0-50°C, 0-100% UR

### **LM35** 🟣
- Temperatura
- Badge roxo
- Valores: -55 a 150°C

### **BMP280** 🟢
- Pressão atmosférica
- Badge verde
- Valores: 300-1100 hPa

## ⚡ Performance

### **Backend**
- Limite de 1000 registros por consulta
- Filtros otimizados por data
- Índices automáticos do Django

### **Frontend**
- Lazy loading de dados
- Estados de loading
- Tratamento de erros
- Cache de estações

## 🐛 Tratamento de Erros

### **Validação de Dados**
- Data início não pode ser maior que data fim
- Estação obrigatória
- Formato de data válido

### **Erros de API**
- Conexão perdida
- Estação não encontrada
- Formato de data inválido
- Limite de registros excedido

### **Estados de Interface**
- Loading durante requisições
- Mensagens de erro descritivas
- Botões de retry
- Feedback visual

## 🎯 Próximas Melhorias

1. **Exportação**: CSV/Excel das leituras
2. **Gráficos**: Visualização temporal dos dados
3. **Paginação**: Para grandes volumes de dados
4. **Filtros Avançados**: Por tipo de sensor, faixa de valores
5. **Relatórios**: PDF com estatísticas
6. **Cache**: Armazenamento local dos dados
7. **Notificações**: Alertas para valores críticos

## 📊 Exemplo de Uso

1. **Acesse** a aba "Leituras"
2. **Selecione** "Estação Central - São Paulo, SP"
3. **Defina** período: 01/01/2024 a 31/01/2024
4. **Clique** em "Buscar Leituras"
5. **Visualize** as leituras na tabela
6. **Analise** o resumo estatístico

## 🔧 Configurações Técnicas

### **URLs da API**
- Base: `http://localhost:8000/api`
- Leituras: `/sensores/estacoes/{id}/leituras/`
- Estações: `/estacoes/`

### **Formato de Datas**
- **API**: YYYY-MM-DD (ISO 8601)
- **Interface**: DD/MM/YYYY (brasileiro)
- **Conversão**: Automática no serviço

### **Limites**
- **Registros**: 1000 por consulta
- **Período**: Sem limite (limitado pelos dados)
- **Sensores**: Todos os tipos suportados
