<template>
    <div class="gap-4 mt-12 mb-12">
        <div class="mb-10">
            <CreateKeywordClusterBtn @clusterCreated="handleClusterCreated" />
        </div>
        <div v-if="keywordClusters.length > 0" class="w-full">
            <Collapsible v-for="item in keywordClusters" :key="item" class="mb-3">
                <CollapsibleTrigger class="w-full">
                    <div class="border-2 border-gray-300 p-1 px-5 w-full text-left rounded-lg flex items-center">
                        <div> {{ item.name  }} </div>
                        <div class="ml-auto"> <img src="@/assets/img/drop_icon.png" class="w-[20px] opacity-70" /> </div>
                    </div>
                </CollapsibleTrigger>
                <CollapsibleContent class="w-full">
                    <div v-if="item.keywords.length == 0" class="px-3 pt-4">
                        No keywords stored
                    </div>
                    <Table class="my-5">
                        <TableHeader>
                        </TableHeader>
                        <TableBody>
                        <TableRow v-for="keyword in item.keywords" :key="keyword" >
                            <TableCell class="text-sm">
                            {{ keyword }}
                            </TableCell>
                            
                            <TableCell class="flex justify-end gap-2">
                                <Button variant="outline"> Test </Button>
                                <Button variant="destructive"> <img class="h-[15px]" src="@/assets/img/trash_icon.png" /> </Button>
                            </TableCell>
                        </TableRow>
                        </TableBody>
                    </Table>
                </CollapsibleContent>
            </Collapsible>
            
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

import { Button } from '@/components/ui/button'

import CreateKeywordClusterBtn from '@/components/CreateKeywordClusterBtn.vue'


import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

import SaveToKeywordcluster from '@/components/SaveToKeywordCluster.vue'

const keywordClusters = ref("");


const fetchKeywordClusters = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/api/get_keywords_clusters",
            {
                headers: {
                    Authorization: `Bearer ${token}`

                },
            });
        keywordClusters.value = response.data.clusters;
        console.log(keywordClusters.value);
    } catch (error) {
        console.error("Error fetching keywords clusters:", error);
    }
};

const handleClusterCreated = () => {
    fetchKeywordClusters();
};

onMounted(async () => {
    fetchKeywordClusters();
});








</script>
