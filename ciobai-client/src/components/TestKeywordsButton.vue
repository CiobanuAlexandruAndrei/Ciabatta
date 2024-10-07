<template>
    <DropdownMenu :open="restOpen" @update:open="setNotVisible">
        <DropdownMenuTrigger>
            <Button variant="outline" :class="buttonClasses" class="flex gap-2">
                <div v-if="variant == 'all'" class="h-full">
                    <img src="@/assets/img/test_all_icon.png" class="h-full opacity-70" />
                </div>
                <div v-if="variant == 'one'" class="h-full">
                    <img src="@/assets/img/test_icon.png" class="h-full opacity-70" />
                </div>
                <div v-if="buttonText">
                    {{ buttonText }}
                </div>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent :class="{'w-[300px]': !hasKeywordData, 'w-full': hasKeywordData}" class="mr-10 max-w-screen-lg">
            <div class="p-1">
                <Select v-if="!dataRetrieved" v-model="selectedCountry">
                    <SelectTrigger class="w-full">
                        <SelectValue placeholder="Country" />
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
                <ScrollArea class="h-[300px] w-full p-4 px-4" v-if="keywordData.length > 0 && !isLoading">
                    <KeywordDataTable
                        :keywordData="keywordData"
                        :isLoading="isLoading"
                        :keywordClusters="keywordClusters"
                        @clusterCreated="handleClusterCreated"
                    />
                </ScrollArea>
                <div v-if="isLoading">
                    <img src="@/assets/img/dots-loading.gif" class="h-[35px]" />
                </div>
            </div>
            <Button v-if="!dataRetrieved" type="submit" variant="outline" class="p-1 text-xs h-8 w-full" @click="searchKeywords"> Start </Button>
        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script setup>
import { ref, onMounted, defineProps, defineEmits, computed } from 'vue';
import axios from 'axios';
import { Toaster } from '@/components/ui/toast';
import { Button } from '@/components/ui/button';
import KeywordDataTable from '@/components/KeywordDataTable.vue';
import { ScrollArea } from '@/components/ui/scroll-area';

import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useToast } from '@/components/ui/toast/use-toast';

const props = defineProps(['keywords', 'buttonClasses', 'buttonText', 'variant']);
const emit = defineEmits(['clusterCreated']);

const keywordData = ref([]);
const isLoading = ref(false);
const noInfoFound = ref(false);
const keywordClusters = ref([]);
const countries = ref([]);
const selectedCountry = ref('');
const restOpen = ref(false);
const dataRetrieved = ref(false);

const fetchCountries = async () => {
    try {
        const response = await axios.get('https://restcountries.com/v3.1/all');
        countries.value = response.data.sort((a, b) => a.name.common.localeCompare(b.name.common));
    } catch (error) {
        console.error('Error fetching countries:', error);
    }
};

const fetchKeywordClusters = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/api/get_keywords_clusters', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        keywordClusters.value = response.data.clusters;
    } catch (error) {
        console.error('Error fetching keyword clusters:', error);
    }
};

const searchKeyword = async (keyword) => {
    try {
        const token = localStorage.getItem('token');
        const csrf = localStorage.getItem('csrf');
        const response = await axios.post(
            'http://127.0.0.1:5000/api/search_keyword',
            {
                csrf_token: csrf,
                name: keyword,
                country: selectedCountry.value,
                limit: 1,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }
        );

        if (response.status == 200) {
            const result = response.data.result.map((item) => ({
                keyword: item.keyword,
                volume: item.keyword_info.search_volume || 'Unknown',
                competition: item.keyword_info.competition_level || 'Unknown',
                difficulty: item.keyword_properties.keyword_difficulty || 'Unknown',
                intent: item.search_intent_info.main_intent,
                trend: item.keyword_info.trend,
            }));
            keywordData.value.push(...result);
        } else if (response.status == 204) {
            noInfoFound.value = true;
        }
    } catch (error) {
        console.error('Error searching keyword:', error);
    }
};

const searchKeywords = async () => {
    if (!selectedCountry.value) {
        alert('Please select a country');
        return;
    }

    isLoading.value = true;
    keywordData.value = [];

    for (const keyword of props.keywords) {
        await searchKeyword(keyword);
    }

    isLoading.value = false;
    dataRetrieved.value = true;
};

const handleClusterCreated = () => {
    emit('clusterCreated');
};

const setNotVisible = () => {
    restOpen.value = !restOpen.value;
};

const hasKeywordData = computed(() => keywordData.value.length > 0);

onMounted(() => {
    fetchCountries();
    fetchKeywordClusters();
});
</script>