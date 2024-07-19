<template>
    <div class="max-w-full">
        <div class="flex gap-1">
            <Button @click="fetchAPIUsage('week')" variant="outline">Last Week</Button>
            <Button @click="fetchAPIUsage('month')" variant="outline">Last Month</Button>
            <Button @click="fetchAPIUsage('year')" variant="outline">Last Year</Button>
        </div>

        <div class="flex mt-8 gap-5 max-w-full">
            <div v-for="([apiName, api], index) in Object.entries(apiUsage)" :key="index" class="flex">
                <div class="h-[400px]">
                    <div class="font-bold"> {{ apiName }} </div>
                    <div>Costs: {{ api.costs.reduce((a, b) => a + b, 0).toFixed(2) }} $ </div>
                    <div>Calls: {{ api.call_counts.reduce((total, current) => total + current, 0) }} </div>
                    <APIUsageLineChart :costs="api.costs" :labels="api.periods" />
                </div>
            </div>
        </div>

        <div class="flex max-w-full">
            <div class="text-center font-bold">
                Costs: {{ costData.reduce((total, current) => total + current, 0) }} $
                <APIUsagePieChart :apiData="costData" :apiLabels="['DataForSEO','OpenAI']" />
            </div>
            <div class="text-center font-bold">
                Calls: {{ callData.reduce((total, current) => total + current, 0) }}
                <APIUsagePieChart :apiData="callData" :apiLabels="['DataForSEO','OpenAI']" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from "axios";
import { Button } from '@/components/ui/button';
import APIUsageLineChart from '@/components/APIUsageLineChart.vue';
import APIUsagePieChart from '@/components/APIUsagePieChart.vue';

const apiUsage = ref({});

const fetchAPIUsage = async (selectedPeriod) => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.post("http://127.0.0.1:5000/api/get_api_usage_costs", {
            period: selectedPeriod,
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        apiUsage.value = response.data.data;
        console.log("Fetched API usage:", apiUsage.value);
    } catch (error) {
        console.error("Error fetching API usage costs:", error);
    }
};

// Compute aggregated data for pie charts
const apiLabels = computed(() => {
    return Object.keys(apiUsage.value);
});

const costData = computed(() => {
    return Object.values(apiUsage.value).map(api =>
        parseFloat(api.costs.reduce((total, cost) => total + cost, 0).toFixed(2))
    );
});

const callData = computed(() => {
    return Object.values(apiUsage.value).map(api =>
        api.call_counts.reduce((total, count) => total + count, 0)
    );
});

onMounted(() => {
    fetchAPIUsage("week");
});
</script>