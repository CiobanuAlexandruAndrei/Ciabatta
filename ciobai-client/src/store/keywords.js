import { defineStore } from 'pinia';
import axios from 'axios';

export const useKeywordsStore = defineStore({
  id: 'keywords',
  state: () => ({
    countries: [],
    keyword: '',
    selectedCountry: '',
    keywordData: [],
    isLoading: false,
    noInfoFound: false,
    keywordClusters: [],
  }),
  actions: {
    async fetchCountries() {
      try {
        const response = await axios.get('https://restcountries.com/v3.1/all');
        this.countries = response.data.sort((a, b) =>
          a.name.common.localeCompare(b.name.common)
        );
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    },
    async searchKeyword() {
      this.isLoading = true;
      this.noInfoFound = false;
      const token = localStorage.getItem('token');
      const csrf = localStorage.getItem('csrf');

      try {
        const response = await axios.post(
          'http://127.0.0.1:5000/api/search_keyword',
          {
            csrf_token: csrf,
            name: this.keyword,
            country: this.selectedCountry,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          }
        );

        if (response.status === 200) {
          console.log(response.data);
          this.keywordData = response.data.result.map(item => ({
            keyword: item.keyword,
            volume: item.keyword_info.search_volume || 'Unknown',
            competition: item.keyword_info.competition_level || 'Unknown',
            difficulty: item.keyword_properties.keyword_difficulty || 'Unknown',
            intent: item.search_intent_info.main_intent,
            trend: item.keyword_info.trend,
          }));
        } else if (response.status === 204) {
          this.noInfoFound = true;
        }
        this.isLoading = false;
      } catch (error) {
        console.error('Error searching keyword:', error);
        this.isLoading = false;
        this.noInfoFound = true;
      }
    },
    async fetchKeywordClusters() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/api/get_keywords_clusters', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.keywordClusters = response.data.clusters;
      } catch (error) {
        console.error('Error fetching keywords clusters:', error);
      }
    },
    handleClusterCreated() {
      this.fetchKeywordClusters();
    },
    setKeyword(value) {
      this.keyword = value;
    },
    setSelectedCountry(value) {
      this.selectedCountry = value;
    }
  },
});