# 🔍 Tabela Avançada de Leituras - Ordenação e Busca

Implementação de funcionalidades avançadas na tabela de leituras: **ordenação de colunas** e **busca global**.

## ✨ Funcionalidades Implementadas

### 🔍 **Busca Global**
- **Campo de Busca**: Input com ícone de lupa
- **Busca em Todas as Colunas**: ID, Sensor, Medida, Valor, Unidade, Data/Hora
- **Busca em Tempo Real**: Filtragem instantânea conforme digitação
- **Botão Limpar**: Remove o filtro de busca com um clique
- **Contador de Resultados**: Mostra "X de Y leituras" encontradas

### 📊 **Ordenação de Colunas**
- **Clique nas Colunas**: Ordena clicando no cabeçalho da coluna
- **Indicadores Visuais**: Setas ↑↓ mostram a direção da ordenação
- **Coluna Ativa**: Destaque visual da coluna sendo ordenada
- **Controles Manuais**: Dropdown + botão para ordenação
- **Alternância**: Clique novamente para inverter a ordem

### 🎨 **Interface Moderna**
- **Controles Integrados**: Busca e ordenação na mesma barra
- **Design Responsivo**: Adaptável para desktop e mobile
- **Feedback Visual**: Hover effects e estados ativos
- **Acessibilidade**: Labels e títulos descritivos

## 🚀 Como Usar

### **Busca Global**
1. **Digite** no campo "Buscar em todas as colunas..."
2. **Resultados** aparecem instantaneamente
3. **Clique no ×** para limpar a busca
4. **Contador** mostra quantas leituras foram encontradas

### **Ordenação por Colunas**
1. **Clique** no cabeçalho da coluna desejada
2. **Clique novamente** para inverter a ordem (A→Z ou Z→A)
3. **Use os controles** dropdown + botão para ordenação manual
4. **Indicadores visuais** mostram a coluna e direção ativas

## 🔧 Funcionalidades Técnicas

### **Busca Inteligente**
```javascript
// Busca em todas as colunas
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
```

### **Ordenação por Tipo de Dados**
- **Números**: ID e Valor ordenados numericamente
- **Datas**: Timestamp ordenado cronologicamente  
- **Texto**: Sensor, Medida, Unidade ordenados alfabeticamente
- **Case Insensitive**: Busca e ordenação ignoram maiúsculas/minúsculas

### **Estados da Interface**
- **Loading**: Durante carregamento de dados
- **Vazio**: Quando não há leituras
- **Erro**: Em caso de falha na API
- **Filtrado**: Mostra resultados da busca
- **Ordenado**: Indica coluna e direção ativas

## 📱 Responsividade

### **Desktop (> 768px)**
- Controles em linha horizontal
- Busca com largura máxima de 400px
- Ordenação lado a lado

### **Tablet (768px)**
- Controles empilhados verticalmente
- Busca ocupa toda a largura
- Ordenação em linha

### **Mobile (< 480px)**
- Controles em coluna única
- Input de busca otimizado para touch
- Botões de ordenação em largura total

## 🎯 Exemplos de Uso

### **Buscar por Sensor**
- Digite "DHT11" para ver apenas leituras do sensor DHT11
- Digite "temperatura" para filtrar por medida

### **Ordenar por Valor**
- Clique em "Valor" para ordenar do menor ao maior
- Clique novamente para inverter (maior ao menor)

### **Buscar por Data**
- Digite "2024" para ver leituras de 2024
- Digite "15/01" para filtrar por data específica

### **Combinação de Filtros**
- Busque "DHT11" + ordene por "Valor"
- Busque "temperatura" + ordene por "Data/Hora"

## 🔍 Tipos de Busca Suportados

### **Por ID**
- Exemplo: "123" → mostra leitura com ID 123

### **Por Sensor**
- Exemplo: "DHT11" → todas as leituras do DHT11
- Exemplo: "dht" → sensores que contenham "dht"

### **Por Medida**
- Exemplo: "temperatura" → todas as medidas de temperatura
- Exemplo: "umidade" → todas as medidas de umidade

### **Por Valor**
- Exemplo: "25" → leituras com valor 25
- Exemplo: "30.5" → leituras com valor 30.5

### **Por Unidade**
- Exemplo: "°C" → todas as leituras em Celsius
- Exemplo: "%" → todas as leituras em percentual

### **Por Data/Hora**
- Exemplo: "2024" → leituras de 2024
- Exemplo: "15/01" → leituras do dia 15/01
- Exemplo: "10:30" → leituras às 10:30

## 📊 Resumo Dinâmico

O resumo estatístico se adapta aos filtros aplicados:

- **Total**: "X de Y leituras" (filtradas de total)
- **Sensores Únicos**: Conta apenas sensores dos resultados filtrados
- **Período**: Data da primeira à última leitura filtrada
- **Filtro Ativo**: Mostra o termo de busca quando aplicado

## 🎨 Indicadores Visuais

### **Cabeçalhos Ordenáveis**
- **Cursor**: Pointer ao passar o mouse
- **Hover**: Fundo cinza claro
- **Ativo**: Fundo azul claro + texto azul
- **Seta**: ↑ para crescente, ↓ para decrescente

### **Campo de Busca**
- **Ícone**: 🔍 à esquerda
- **Focus**: Borda azul + sombra
- **Limpar**: Botão × à direita (só aparece com texto)

### **Controles de Ordenação**
- **Dropdown**: Lista todas as colunas
- **Botão**: Alterna entre ↑ e ↓
- **Ativo**: Botão azul quando ordenação aplicada

## ⚡ Performance

### **Busca Otimizada**
- Filtragem em tempo real
- Busca case-insensitive
- Conversão de tipos automática

### **Ordenação Eficiente**
- Algoritmo de ordenação nativo do JavaScript
- Tratamento especial por tipo de dados
- Preservação da busca durante ordenação

### **Interface Responsiva**
- Re-renderização apenas quando necessário
- Estados computados para performance
- Debounce implícito na busca

## 🔧 Configurações Técnicas

### **Campos de Busca**
- ID, Sensor, Medida, Valor, Unidade, Data/Hora
- Busca case-insensitive
- Suporte a números e texto

### **Campos de Ordenação**
- ID (numérico)
- Sensor (alfabético)
- Medida (alfabético)
- Valor (numérico)
- Unidade (alfabético)
- Timestamp (cronológico)

### **Estados Persistidos**
- Busca mantida durante ordenação
- Ordenação mantida durante busca
- Reset ao trocar de estação

## 🎯 Próximas Melhorias

1. **Busca Avançada**: Filtros por faixa de valores
2. **Salvamento**: Manter preferências de ordenação
3. **Exportação**: Exportar resultados filtrados
4. **Histórico**: Últimas buscas realizadas
5. **Atalhos**: Teclas de atalho para ordenação
6. **Busca por Regex**: Suporte a expressões regulares
7. **Filtros Múltiplos**: Combinação de critérios
8. **Busca Inteligente**: Sugestões automáticas

## 📝 Notas de Implementação

- **Vue.js 3**: Composition API com reatividade
- **CSS Grid/Flexbox**: Layout responsivo moderno
- **JavaScript Nativo**: Sem dependências externas
- **Acessibilidade**: ARIA labels e navegação por teclado
- **Performance**: Computed properties otimizadas
