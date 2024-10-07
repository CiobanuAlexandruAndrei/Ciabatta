import { defineStore } from 'pinia';
import axios from 'axios';

export const useKeywordGeneratorStore = defineStore({
  id: 'keywordGenerator',
  state: () => ({
    topicName: '',
    intentName: '',
    additionalInstructions: '',
    keywords: [],
    isLoading: false,
    keywordClusters: [],
  }),
  actions: {
    setTopicName(topicName) {
      this.topicName = topicName;
    },
    setIntentName(intentName) {
      this.intentName = intentName;
    },
    setAdditionalInstructions(additionalInstructions) {
      this.additionalInstructions = additionalInstructions;
    },
    async generateKeywords() {
      this.isLoading = true;
      const token = localStorage.getItem('token');

      try {
        const response = await axios.post(
          'http://127.0.0.1:5000/api/generate_keyword_suggestions',
          {
            topic: this.topicName,
            intent: this.intentName,
            additional_instructions: this.additionalInstructions,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          }
        );

        if (response.data && response.data.result) {
          this.keywords = response.data.result.keywords;
        }
      } catch (error) {
        console.error('Error generating keywords:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchKeywordClusters() {
      const token = localStorage.getItem('token');

      try {
        const response = await axios.get('http://127.0.0.1:5000/api/get_keywords_clusters', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.data && response.data.clusters) {
          this.keywordClusters = response.data.clusters;
        }
      } catch (error) {
        console.error('Error fetching keyword clusters:', error);
      }
    },

    handleClusterCreated() {
      this.fetchKeywordClusters();
    },
  },
});