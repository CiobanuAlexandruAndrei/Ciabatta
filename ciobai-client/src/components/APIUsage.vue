<template>
    <div>
        <div v-for="(costs, api) in apiUsage" :key="api" class="mb-5">
            
            <b>{{ api }}</b>
            <p>Total Cost: {{ computeTotalCost(costs) }} USD</p>
            <p>Total Calls: {{ costs.length }}</p>
        </div>
        {{ apiUsage }}
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const apiUsage = ref({});

const fetchAPIUsage = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/get-api-usage-costs", {
            headers: {
                Authorization: `Token ${token}`
            },
        });
        
        apiUsage.value = response.data.data;
    } catch (error) {
        console.error("Error fetching API usage costs:", error);
    }
};

const computeTotalCost = (costs) => {
    return costs.reduce((total, record) => total + record.cost, 0).toFixed(6);
};

onMounted(() => {
    fetchAPIUsage();
});
</script>