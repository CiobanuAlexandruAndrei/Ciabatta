<template>
    <Toaster />
    <DropdownMenu :open="restOpen" @update:open="setNotVisible">
        <DropdownMenuTrigger> <Button> Save </Button> </DropdownMenuTrigger>
        <DropdownMenuContent class="w-[200px]">
            <DropdownMenuLabel> Save to cluster </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <CreateKeywordClusterBtn @clusterCreated="handleClusterCreated" />
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
            <Button type="submit" class="p-1 text-xs h-8 w-full" @click="addKeywordToCluster()"> Save </Button>

        </DropdownMenuContent>
    </DropdownMenu>
</template>
<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Toaster } from '@/components/ui/toast'
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
import { useToast } from '@/components/ui/toast/use-toast'

import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"

const props = defineProps(['keyword'])
const selectedClusterId = ref("");
const keywordClusters = ref("");

const showSelectClusterAlert = ref(false);
const restOpen = ref(false);

const { toast } = useToast()


const fetchKeywordClusters = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/get-keyword-clusters", {
            headers: {
                Authorization: `Token ${token}`
            },
        });
        keywordClusters.value = response.data.clusters;
    } catch (error) {
        console.error("Error fetching keywords clusters:", error);
    }
};

const addKeywordToCluster = async () => {
    console.log(selectedClusterId.value);
    console.log(props.keyword);

    if (!selectedClusterId.value) {
        showSelectClusterAlert.value = true;
        console.log('Please select a cluster.');
        return;
    }

    try {
        const token = localStorage.getItem("token");
        const response = await axios.post("http://127.0.0.1:8000/api/add-keyword-to-cluster", {
            keyword_name: props.keyword,
            cluster_id: selectedClusterId.value
        }, {
            headers: {
                Authorization: `Token ${token}`,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        if (response.status === 201) {
            console.log('Keyword added to cluster successfully');
            restOpen.value = false;
            toast({
                class: 'top-0 right-0 flex fixed md:max-w-[420px] md:top-4 md:right-4 shadow-none',
                description: 'Success, Keyword added to cluster successfully!',
            });

            // Optionally, you can add some UI feedback here
        } else {
            console.error('Error adding keyword to cluster:', response.data.message);
        }
    } catch (error) {
        console.error("Error adding keyword to cluster:", error);
    }
}

const handleClusterCreated = () => {
    fetchKeywordClusters();
};

const setNotVisible = () => {
    restOpen.value = !restOpen.value;
}

onMounted(() => {
    fetchKeywordClusters();
});

</script>