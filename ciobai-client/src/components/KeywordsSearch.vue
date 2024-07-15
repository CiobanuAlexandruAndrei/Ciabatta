<template>
    <div class="flex gap-4 mt-12 mb-12">
        <Input v-model="keyword" type="text" placeholder="Keyword" class="w-[300px]" />
        <Select v-model="selectedCountry">
            <SelectTrigger class="w-[280px]">
                <SelectValue placeholder="Select a country" />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    <SelectLabel>Countries</SelectLabel>
                    <template v-for="country in countries" :key="country.name.common">
                        <SelectItem :value="country.name.common">
                            <img :src="country.flags.svg" alt="" class="inline-block w-6 h-4 mr-2" />
                            {{ country.name.common }}
                        </SelectItem>
                    </template>
                </SelectGroup>
            </SelectContent>
        </Select>
        <Button @click="searchKeyword" variant="secondary">
            Search
        </Button>
    </div>

    <Table v-if="keywordData.length > 0">
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
                <TableCell> {{ item.volume }} </TableCell>
                <TableCell> 
                    <span :class="[getCompetitionColor(item.competition), 'p-1', 'rounded']">
                        {{ item.competition }} 
                    </span>    
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
                    <Button @click="saveKeyword(item.keyword)">Save</Button>
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

// Importing the image assets
import upIcon from '@/assets/img/up_icon.png';
import downIcon from '@/assets/img/down_icon.png';
import rightIcon from '@/assets/img/right_icon.png';

const countries = ref([]);
const keyword = ref("");
const selectedCountry = ref("");
const keywordData = ref([]);

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

const saveKeyword = async (keyword) => {
    /*
    const token = localStorage.getItem("token");
    try {
        await axios.post(
            "http://127.0.0.1:8000/api/save-keyword",
            { name: keyword },
            {
                headers: {
                    Authorization: `Token ${token}`,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );
    } catch (error) {
        console.error("Error saving keyword:", error);
    }
    */
};

const searchKeyword = async () => {
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

        keywordData.value = response.data.result.map(item => ({
            keyword: item.keyword_data.keyword,
            volume: item.keyword_data.keyword_info.search_volume, 
            competition: item.keyword_data.keyword_info.competition_level,
            difficulty: item.keyword_data.keyword_properties.keyword_difficulty,
            intent: item.keyword_data.search_intent_info.main_intent,
            trend: item.keyword_data.trend
        }));

    } catch (error) {
        console.error("Error searching keyword:", error);
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
    }
}


const getDifficultyColor = (difficulty) => {
    if (difficulty >= 0 && difficulty < 30){
        return 'bg-green-400';
    } else if (difficulty >= 30 && difficulty < 50) {
        return 'bg-amber-200';
    } else if (difficulty >= 50 && difficulty <= 100) {
        return 'bg-rose-400';
    }
}

onMounted(() => {
    fetchCountries();
});
</script>