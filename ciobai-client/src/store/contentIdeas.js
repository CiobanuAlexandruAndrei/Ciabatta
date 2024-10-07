import { defineStore } from 'pinia';
import axios from 'axios';
import jsonAutocomplete from 'json-autocomplete';

export const useContentIdeasStore = defineStore({
  id: 'contentIdeas',
  state: () => ({
    topic: '',
    additionalInstructions: '',
    ideas: { topics: [] },
    isLoading: false,
  }),
  actions: {
    setTopic(value) {
      this.topic = value;
    },
    setAdditionalInstructions(value) {
      this.additionalInstructions = value;
    },
    async generateIdeas() {
      this.isLoading = true;
      const token = localStorage.getItem('token');

      console.log('Starting to generate ideas...');
      console.log('Topic:', this.topic);
      console.log('Additional Instructions:', this.additionalInstructions);

      try {
        const response = await fetch('http://127.0.0.1:5000/api/generate_content_ideas', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            topic: this.topic,
            additional_instructions: this.additionalInstructions,
          }),
        });

        console.log('Response received:', response);

        if (!response.body) {
          throw new Error('ReadableStream not yet supported in this browser.');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let jsonResponse = '';

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          jsonResponse += decoder.decode(value, { stream: true });

          try {
            const completeJsonString = jsonAutocomplete(jsonResponse);
            let parsedJson = completeJsonString;

            parsedJson = parsedJson.replace(/json/g, '');
            parsedJson = parsedJson.replace('```', '');

            parsedJson = JSON.parse(parsedJson);
            this.ideas = parsedJson;
            console.log(parsedJson);
          } catch (error) {
            console.error('Error parsing JSON:', error);
          }
        }
      } catch (error) {
        console.error('Error fetching ideas:', error);
      } finally {
        console.log('Finished generating ideas.');
        this.isLoading = false;
      }
    },
  },
});