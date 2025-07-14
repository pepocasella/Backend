<script setup>
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell
} from '@/components/ui/table'

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select'

import { ref, computed, onMounted } from 'vue'

const leituras = ref([])
const sensorSelecionado = ref('')

// Busca os dados da API
async function fetchLeituras() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/sensores/estacoes/1/leituras/')
    const json = await response.json()
    leituras.value = json
  } catch (error) {
    console.error('Erro ao buscar dados da estação:', error)
  }
}

// Computa os dados filtrados conforme o sensor selecionado
const leiturasFiltradas = computed(() => {
  if (!sensorSelecionado.value) return leituras.value
  return leituras.value.filter(item => item.sensor === sensorSelecionado.value)
})

// Formata a data/hora
function formatData(iso) {
  const d = new Date(iso)
  return d.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
}

onMounted(() => {
  fetchLeituras()
})
</script>

<template>



  <div class="p-4 space-y-4">
    <h2 class="text-xl font-bold">Leituras dos Sensores</h2>

  <Select v-model="sensorSelecionado">
    <SelectTrigger>
      <SelectValue placeholder="Escolha um sensor" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="DHT11">DHT11</SelectItem>
      <SelectItem value="LM35">LM35</SelectItem>
    </SelectContent>
  </Select>

  <p class="mt-4">Selecionado: {{ sensorSelecionado }}</p>


<div class="p5"></div>
    <!-- Tabela -->
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>Sensor</TableHead>
          <TableHead>Medida</TableHead>
          <TableHead>Valor</TableHead>
          <TableHead>Unidade</TableHead>
          <TableHead>Data</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        <TableRow v-for="item in leiturasFiltradas" :key="item.id">
          <TableCell>{{ item.id }}</TableCell>
          <TableCell>{{ item.sensor }}</TableCell>
          <TableCell>{{ item.medida }}</TableCell>
          <TableCell>{{ item.valor }}</TableCell>
          <TableCell>{{ item.unidade }}</TableCell>
          <TableCell>{{ formatData(item.timestamp) }}</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>