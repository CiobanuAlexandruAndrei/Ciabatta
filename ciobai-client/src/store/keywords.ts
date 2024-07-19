import { defineStore } from 'pinia';

export const useKeywordsStore = defineStore({
    id: 'keywords',
    state: () => ({
        countries: [],
        keyword: "",
        selectedCountry: "",
        keywordData: [],
        isLoading: false,
        noInfoFound: false,
        keywordClusters: [],
    }),
    actions: {
        async fetchCountries() {
            // Move the fetchCountries logic here
        },
        async searchKeyword() {
            // Move the searchKeyword logic here
        },
        async fetchKeywordClusters() {
            // Move the fetchKeywordClusters logic here
        },
        handleClusterCreated() {
            // Move the handleClusterCreated logic here
        },
    },
});
