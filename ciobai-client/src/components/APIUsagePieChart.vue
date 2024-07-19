<template>
    <Pie :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { ref, watch } from 'vue';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  apiData: {
    type: Array,
    required: true
  },
  apiLabels: {
    type: Array,
    required: true
  }
})

const chartData = ref({
    labels: props.apiLabels,
    datasets: [
        {
            backgroundColor: ['#9ede38', '#22aa87'],
            data: props.apiData
        }
    ]
})

const chartOptions = ref({
    responsive: true,
    maintainAspectRatio: true,
    layout: {
        padding: 20
    }
})

// Deep watch on apiData
watch(
  () => props.apiData,
  (newData) => {
    chartData.value = {
      ...chartData.value,
      datasets: [{
        ...chartData.value.datasets[0],
        data: newData
      }]
    };
  },
  { deep: true }
);

// Deep watch on apiLabels
watch(
  () => props.apiLabels,
  (newLabels) => {
    chartData.value = {
      ...chartData.value,
      labels: newLabels
    };
  },
  { deep: true }
);
</script>