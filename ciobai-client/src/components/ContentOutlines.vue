<template>
    <div class="mt-8 p-4">
        <div class="bg-white">
            <router-link :to="'/content-outline/' + task.id" v-for="task in contentOutlinesTasks" :key="task.id" class="flex justify-between items-center border-b last:border-b-0 py-3">
                <div 
                    
                    class="text-slate-700 text-sm hover:underline w-1/3 text-left"
                >
                    <span class="font-semibold">{{ task.content_outline.title }}</span>
                </div>

                <div class="flex justify-center w-1/3">
                    <span 
                        :class="{
                            'bg-green-200 text-green-800': task.content_outline_task_status === 'Completed',
                            'bg-red-200 text-red-800': task.content_outline_task_status === 'Failed',
                            'bg-yellow-200 text-yellow-800': task.content_outline_task_status === 'Processing'
                        }"
                        class="inline-flex items-center px-3 py-1 text-sm font-medium rounded-full"
                    >
                        {{ task.content_outline_task_status }}
                    </span>
                </div>

                <span class="text-gray-500 w-1/3 text-right">{{ timeSince(task.added) }}</span>
            </router-link>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';
import axios from "axios";

const router = useRouter();
const contentOutlinesTasks = ref([]);


const fetchContentOutlinesTasks = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/api/get_all_content_outlines_tasks", {
            headers: {
                Authorization: `Bearer ${token}`
            },
        });
        contentOutlinesTasks.value = response.data.result;
        console.log(contentOutlinesTasks.value);
    } catch (error) {
        console.error("Error fetching content outlines tasks:", error);
    }
};


const timeSince = (date) => {
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);
    let interval = Math.floor(seconds / 31536000);
    if (interval > 1) return `${interval} years ago`;
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) return `${interval} months ago`;
    interval = Math.floor(seconds / 86400);
    if (interval > 1) return `${interval} days ago`;
    interval = Math.floor(seconds / 3600);
    if (interval > 1) return `${interval} hours ago`;
    interval = Math.floor(seconds / 60);
    if (interval > 1) return `${interval} minutes ago`;
    return "just now";
};

onMounted(async () => {
    fetchContentOutlinesTasks();
});
</script>

<style scoped>

</style>
