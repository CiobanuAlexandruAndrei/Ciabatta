<template>
    <canvas ref="canvas" class="h-full w-full max-h-[300px]"></canvas>
</template>

<script setup>
import { ref, defineProps, watch, onMounted } from 'vue';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    LineController,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    LineController,
    Title,
    Tooltip,
    Legend
);

const props = defineProps({
    costs: Array,
    labels: Array
});

const chartOptions = ref({
    responsive: true,
    maintainAspectRatio: true,
    layout: {
        scales: {
            x: {
                offset: true,
            }
        },
    }
});

const chartData = ref({
    labels: props.labels,
    datasets: [
        {
            label: 'Costs (USD)',
            backgroundColor: '#32CD32',
            data: props.costs,
            pointRadius: 5
        }
    ]
});

const canvas = ref(null);
let chartInstance = null;

const renderChart = () => {
    if (canvas.value) {
        if (chartInstance) {
            chartInstance.destroy();
        }
        chartInstance = new ChartJS(canvas.value, {
            type: 'line',
            data: chartData.value,
            options: chartOptions.value
        });
    }
};

watch(
    () => [props.costs, props.labels],
    () => {
        chartData.value.labels = props.labels;
        chartData.value.datasets[0].data = props.costs;
        renderChart();
    }
);

onMounted(() => {
    renderChart();
});
</script>

<style scoped>
/* Add any necessary styles */
</style>