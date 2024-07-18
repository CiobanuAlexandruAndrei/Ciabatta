<template>
    <Table v-if="keywordData.length > 0 && !isLoading">
        <TableCaption></TableCaption>
        <TableHeader>
            <TableRow>
                <TableHead class="w-[100px]"> Name </TableHead>
                <TableHead>Trend</TableHead>
                <TableHead>Volume</TableHead>
                <TableHead>Competition</TableHead>
                <TableHead>Difficulty</TableHead>
                <TableHead>Intent</TableHead>
                <TableHead class="text-right"> Actions </TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            <TableRow v-for="item in keywordData" :key="item.keyword">
                <TableCell class="font-medium w-[300px]">
                    {{ item.keyword }}
                </TableCell>
                <TableCell>
                    <img :src="getTrendIcon(item.trend)" alt="trend icon" class="h-5 text-center" />
                </TableCell>
                <TableCell> 
                    <div v-if="item.volume">
                        {{ item.volume }}
                    </div>
                    <div v-else>
                        Unknown
                    </div>
                </TableCell>
                <TableCell> 
                    <div v-if="item.competition">
                        <span :class="[getCompetitionColor(item.competition), 'p-1', 'rounded']">
                            {{ item.competition }} 
                        </span>    
                    </div>
                    <div v-else>
                        <span class="bg-slate-300 p-1 rounded">
                            Unknown
                        </span>
                    </div>
                </TableCell>
                <TableCell> 
                    <div v-if="item.difficulty">
                        <span :class="[getDifficultyColor(item.difficulty), 'p-1', 'rounded']">
                            {{ item.difficulty }} 
                        </span>
                    </div>
                    <div v-else>
                        <span class="bg-slate-300 p-1 rounded">
                            Unknown
                        </span>
                    </div>
                </TableCell>
                <TableCell> {{ item.intent }} </TableCell>
                <TableCell class="text-right">
                    <SaveToKeywordCluster variant="save" buttonClasses="bg-green-300 hover:bg-green-400" @clusterCreated="handleClusterCreated" :keyword="item.keyword" :keywordClusters="keywordClusters" />
                </TableCell>
            </TableRow>
        </TableBody>
    </Table>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

import SaveToKeywordCluster from '@/components/SaveToKeywordCluster.vue';
import upIcon from '@/assets/img/up_icon.png';
import downIcon from '@/assets/img/down_icon.png';
import rightIcon from '@/assets/img/right_icon.png';

const props = defineProps({
    keywordData: Array,
    isLoading: Boolean,
    keywordClusters: Array
});
const emit = defineEmits(['clusterCreated']);

const getTrendIcon = (trend) => {
    if (trend === "UP") {
        return upIcon;
    } else if (trend === "DOWN") {
        return downIcon;
    } else if (trend === "SAME") {
        return rightIcon;
    }
};

const getCompetitionColor = (competition) => {
    if (competition === 'HIGH'){
        return 'bg-rose-400';
    } else if (competition === "MEDIUM") {
        return 'bg-amber-200';
    } else if (competition === "LOW") {
        return 'bg-green-400';
    } else {
        return 'bg-slate-300';
    }
}

const getDifficultyColor = (difficulty) => {
    if (difficulty >= 0 && difficulty < 30){
        return 'bg-green-400';
    } else if (difficulty >= 30 && difficulty < 50) {
        return 'bg-amber-200';
    } else if (difficulty >= 50 && difficulty <= 100) {
        return 'bg-rose-400';
    } else {
        return 'bg-slate-300';
    }
}

const handleClusterCreated = () => {
    emit("clusterCreated");
};
</script>