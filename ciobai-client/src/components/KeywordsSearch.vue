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
    <KeywordDataTable
        v-if="keywordData.length > 0 && !isLoading"
        :keywordData="keywordData"
        :isLoading="isLoading"
        :keywordClusters="keywordClusters"
        @clusterCreated="handleClusterCreated"
    />
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

import SaveToKeywordCluster from '@/components/SaveToKeywordCluster.vue'
import LoadingTable from '@/components/LoadingTable.vue'
import KeywordLookupInfo from '@/components/KeywordLookupInfo.vue'
import KeywordDataTable from '@/components/KeywordDataTable.vue'

const countries = ref([]);
const keyword = ref("");
const selectedCountry = ref("");
const keywordData = ref([]);
const isLoading = ref(false);
const noInfoFound = ref(false);
const keywordClusters = ref([]);

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
    const csrf = localStorage.getItem("csrf");

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/api/search_keyword",
            {
                csrf_token: csrf,
                name: keyword.value,
                country: selectedCountry.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
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

const handleClusterCreated = () => {
    fetchKeywordClusters();
};

const fetchKeywordClusters = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/api/get_keywords_clusters", {
            headers: {
                Authorization: `Bearer ${token}`
            },
        });
        keywordClusters.value = response.data.clusters;
    } catch (error) {
        console.error("Error fetching keywords clusters:", error);
    }
};

onMounted(() => {
    fetchCountries();
    fetchKeywordClusters();
});
</script>