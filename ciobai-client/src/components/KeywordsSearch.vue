<template>
    <div class="flex gap-4 mt-12 mb-3">
        <Input v-model="keyword" type="text" placeholder="Keyword" class="w-[300px]" />
        <Select v-model="selectedCountry">
            <SelectTrigger class="w-[280px]">
                <SelectValue placeholder="Select a country" />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    <SelectLabel>Countries</SelectLabel>
                    <div v-for="country in countries" :key="country.name.common">
                        <SelectItem :value="country.name.common">
                            <img :src="country.flags.svg" alt="" class="inline-block w-6 h-4 mr-2" />
                            {{ country.name.common }}
                        </SelectItem>
                    </div>
                </SelectGroup>
            </SelectContent>
        </Select>
        <Button @click="searchKeyword" variant="secondary">
            Search
        </Button>
        <KeywordLookupInfo />
    </div>
    
    <div v-if="isLoading" class="mt-5">
        <LoadingTable />
    </div>
    <div v-if="noInfoFound" class="mt-5">
        No info found
    </div>
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
                    <SaveToKeywordcluster :keyword="item.keyword" />
                </TableCell>
            </TableRow>
        </TableBody>
    </Table>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

import SaveToKeywordcluster from '@/components/SaveToKeywordCluster.vue'
import LoadingTable from '@/components/LoadingTable.vue'
import KeywordLookupInfo from '@/components/KeywordLookupInfo.vue'

import upIcon from '@/assets/img/up_icon.png';
import downIcon from '@/assets/img/down_icon.png';
import rightIcon from '@/assets/img/right_icon.png';

const countries = ref([]);
const keyword = ref("");
const selectedCountry = ref("");
const keywordData = ref([]);
const isLoading = ref(false);
const noInfoFound = ref(false);

const fetchCountries = async () => {
    try {
        const response = await axios.get("https://restcountries.com/v3.1/all");
        countries.value = response.data.sort((a, b) =>
            a.name.common.localeCompare(b.name.common)
        );
    } catch (error) {
        console.error("Error fetching countries:", error);
    }
};

const searchKeyword = async () => {
    isLoading.value = true;
    noInfoFound.value = false;
    const token = localStorage.getItem("token");
    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/api/search-keyword",
            {
                name: keyword.value,
                country: selectedCountry.value,
            },
            {
                headers: {
                    Authorization: `Token ${token}`,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );
        
        if(response.status == 200){
            console.log(response.data);

            keywordData.value = response.data.result.map(item => ({
                keyword: item.keyword,
                volume: item.keyword_info.search_volume || 'Unknown',
                competition: item.keyword_info.competition_level || 'Unknown',
                difficulty: item.keyword_properties.keyword_difficulty || 'Unknown',
                intent: item.search_intent_info.main_intent,
                trend: item.keyword_info.trend
            }));
            
        } else if(response.status == 204){
            noInfoFound.value = true;
        }
        isLoading.value = false;
    } catch (error) {
        console.error("Error searching keyword:", error);
        isLoading.value = false;
        noInfoFound.value = true;
    }
};

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

onMounted(() => {
    fetchCountries();
});
</script>