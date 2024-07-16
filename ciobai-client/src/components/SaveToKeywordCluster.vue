<template>
    <DropdownMenu>
        <DropdownMenuTrigger> <Button> Save </Button> </DropdownMenuTrigger>
        <DropdownMenuContent class="w-[200px]">
            <DropdownMenuLabel> Save to cluster </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <CreateKeywordClusterBtn class="w-full" />
            <DropdownMenuItem>
                <RadioGroup class="my-3" v-model="selectedClusterId">
                    <div v-for="cluster in keywordClusters" :key="cluster.id">
                        <div className="flex items-center space-x-2">
                            <RadioGroupItem :value="cluster.id" :id="cluster.id"
                                @click="selectedClusterId = cluster.id" />
                            <Label :htmlFor="cluster.id"> {{ cluster.name }} </Label>
                        </div>
                    </div>
                </RadioGroup>
            </DropdownMenuItem>
            <Button class="p-1 text-xs h-8 w-full" @click="addKeywordToCluster()"> Save </Button>

        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";



import { Button } from "@/components/ui/button";
import CreateKeywordClusterBtn from '@/components/CreateKeywordClusterBtn.vue'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"


const props = defineProps(['keyword'])
const selectedClusterId = ref("");
const keywordClusters = ref("");
const showSelectClusterAlert = ref(false);


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

const addKeywordToCluster = () => {
    if (!selectedClusterId.value) {
        console.log('ERRORRRRR');
    }
    console.log(props.keyword);
    console.log(selectedClusterId.value);

}

onMounted(() => {
    fetchKeywordClusters();
});

</script>