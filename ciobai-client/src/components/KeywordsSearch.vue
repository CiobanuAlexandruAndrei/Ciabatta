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
    <KeywordDataTable v-if="keywordData.length > 0 && !isLoading"
        :keywordData="keywordData" :isLoading="isLoading"
        :keywordClusters="keywordClusters" @clusterCreated="handleClusterCreated" />
</template>

<script setup>
import { useKeywordsStore } from '@/store/keywords';
import { ref, computed, onMounted, watch } from 'vue';
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import KeywordDataTable from '@/components/KeywordDataTable.vue'
import LoadingTable from '@/components/LoadingTable.vue'

const keywordsStore = useKeywordsStore();

const keyword = ref(keywordsStore.keyword);
const selectedCountry = ref(keywordsStore.selectedCountry);

watch(keyword, (newValue) => {
    keywordsStore.setKeyword(newValue);
});

watch(selectedCountry, (newValue) => {
    keywordsStore.setSelectedCountry(newValue);
});

const searchKeyword = async () => {
    await keywordsStore.searchKeyword();
};

const handleClusterCreated = () => {
    keywordsStore.handleClusterCreated();
};

onMounted(() => {
    keywordsStore.fetchKeywordClusters();
    keywordsStore.fetchCountries();
});

const countries = computed(() => keywordsStore.countries);
const isLoading = computed(() => keywordsStore.isLoading);
const noInfoFound = computed(() => keywordsStore.noInfoFound);
const keywordData = computed(() => keywordsStore.keywordData);
const keywordClusters = computed(() => keywordsStore.keywordClusters);

</script>