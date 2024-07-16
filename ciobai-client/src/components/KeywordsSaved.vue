<template>
    <div class="flex gap-4 mt-12 mb-12">

        <div v-if="keywordClusters.length > 0">
            <Collapsible class="min-w-full">
                <CollapsibleTrigger class="w-full">
                    <div class="border-2 border-gray-200 p-1 w-full text-left">
                        Can I use this in my project?
                    </div>
                </CollapsibleTrigger>
                <CollapsibleContent class="w-full">
                Yes. Free to use for personal and commercial projects. No attribution
                required.
                </CollapsibleContent>
            </Collapsible>
            <ul v-for="item in keywordClusters" :key="item">
                <li> {{ item }} </li>
            </ul>
        </div>  
        
        <div v-else>
            No keyword clusters
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'


const keywordClusters = ref("");


const fetchKeywordClusters = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/get-keyword-clusters",
            {
                headers: {
                    Authorization: `Token ${token}`

                },
            });
        keywordClusters.value = response.data.clusters;
        console.log(keywordClusters.value);
    } catch (error) {
        console.error("Error fetching keywords clusters:", error);
    }
};

onMounted(async () => {
    fetchKeywordClusters();
});








</script>
