<script setup>

import { ref, onMounted } from 'vue';

const dados = ref() 

async function get_dados_estacao() {
  try {
    const response = await fetch('http://localhost:3000/data')
    const json = await response.json()
    dados.value = json
    console.log('Dados da estação carregados:', dados.value)
  } catch (error) {
    console.error('Erro ao buscar dados da estação:', error)
  }
}

onMounted(() => {
  // chama quando o componente é montado
  get_dados_estacao()
});

</script>

<template>

  <div class="p-4 flex items-center gap-4 justify-center">
    <h1>Estação Meteorologica</h1>
  </div>


  <div>
        <ul>
        <li v-for="dado in dados" :key="dado.id">
          {{ dado }}
        </li>
      </ul>
  </div>

</template>