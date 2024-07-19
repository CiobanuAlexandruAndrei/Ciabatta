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
            <Input v-model="additionalInstructions" placeholder="Additional Instructions" />
            <Button @click="generateKeywords" variant="secondary" class="mt-4">Generate</Button>
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
                                <SaveToKeywordcluster @clusterCreated="handleClusterCreated" variant="save"
                                    buttonClasses="bg-green-300 hover:bg-green-400" :keyword="item"
                                    :keywordClusters="keywordClusters" />
                            </div>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useKeywordGeneratorStore } from '@/store/keywordGenerator';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
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

const keywordGeneratorStore = useKeywordGeneratorStore();

const topicName = computed({
    get: () => keywordGeneratorStore.topicName,
    set: (value) => keywordGeneratorStore.setTopicName(value),
});
const intentName = computed({
    get: () => keywordGeneratorStore.intentName,
    set: (value) => keywordGeneratorStore.setIntentName(value),
});
const additionalInstructions = computed({
    get: () => keywordGeneratorStore.additionalInstructions,
    set: (value) => keywordGeneratorStore.setAdditionalInstructions(value),
});

const generateKeywords = async () => {
    await keywordGeneratorStore.generateKeywords();
};

const handleClusterCreated = () => {
    keywordGeneratorStore.handleClusterCreated();
};

onMounted(async () => {
    await keywordGeneratorStore.fetchKeywordClusters();
});

const isLoading = computed(() => keywordGeneratorStore.isLoading);
const keywords = computed(() => keywordGeneratorStore.keywords);
const keywordClusters = computed(() => keywordGeneratorStore.keywordClusters);
</script>