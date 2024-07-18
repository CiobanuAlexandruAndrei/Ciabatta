<template>
    <div>
        <div class="flex gap-4 mt-12 mb-4">
            <Input v-model="topicName" placeholder="Topic or Keyword" />
        
            <Select v-model="intentName">
                <SelectTrigger>
                    <SelectValue placeholder="Intent" />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="informational">Informational</SelectItem>
                        <SelectItem value="commercial">Commercial</SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
        </div>
        <div>
            <Input v-model="additionaInstructions" placeholder="Additional Instructions" />
            <Button @click="generateKeywords()" variant="secondary" class="mt-4">Generate</Button>
        </div>
        <div v-if="isLoading" class="mt-5">
            <LoadingTable />
        </div>
        <div v-if="keywords.length > 0 && !isLoading" class="mt-8">
            <TestKeywordsButton :keywords="keywords" variant="all" buttonText="Test All" buttonClasses="text-xs" />
            <Table class="mt-3">
                <TableHeader>
                    <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead class="text-right">Action</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow v-for="item in keywords" :key="item">
                        <TableCell class="text-sm">{{ item }}</TableCell>
                        <TableCell class="">
                            <div class="flex justify-end gap-1">
                                <TestKeywordsButton variant="one" :keywords="[item]" />
                                <SaveToKeywordcluster @clusterCreated="handleClusterCreated" variant="save" buttonClasses="bg-green-300 hover:bg-green-400"  :keyword="item" :keywordClusters="keywordClusters" />
                            </div>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import SaveToKeywordcluster from '@/components/SaveToKeywordCluster.vue';
import LoadingTable from '@/components/LoadingTable.vue';
import TestKeywordsButton from '@/components/TestKeywordsButton.vue';

import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

const topicName = ref("");
const intentName = ref("");
const additionaInstructions = ref("");
const keywords = ref([]);
const isLoading = ref(false);
const keywordClusters = ref([]);

const generateKeywords = async () => {
    isLoading.value = true;
    const token = localStorage.getItem("token");
    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/api/generate_keyword_suggestions",
            {
                topic: topicName.value,
                intent: intentName.value,
                additional_instructions: additionaInstructions.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );

        keywords.value = response.data.result.keywords;
        isLoading.value = false;

    } catch (error) {
        console.error("Error generating keyword:", error);
        isLoading.value = false;
    }
};

const handleClusterCreated = () => {
    // Refresh components by re-fetching the keyword clusters
    fetchKeywordClusters();
};


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
    } catch (error) {
        console.error("Error fetching keywords clusters:", error);
    }
};

onMounted(async () => {
    fetchKeywordClusters();
});
</script>