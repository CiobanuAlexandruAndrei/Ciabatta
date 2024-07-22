<template>
    <div class="mt-12 mb-3">
        <div class="flex flex-wrap gap-3 w-full mb-12">
            <Input v-model="topic" type="text" placeholder="Keyword or Topic" class="w-[300px]" />
            <Input v-model="additionalInstructions" placeholder="Additional Instructions" class="w-full" />
            <Button @click="generateIdeas" variant="secondary">
                Search
            </Button>
        </div>

        <div v-if="isLoading">
            <LoadingTable />
        </div>

        <div v-if="Object.keys(ideas).length > 0" class="mt-8">
            <Table class="mt-3 w-full">
                <TableHeader>
                    <TableRow>
                        <TableHead>Semantically Related Topic</TableHead>
                        <TableHead>Variations on the Topic</TableHead>
                        <TableHead>Clickbait Style Title</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <template v-for="(idea, topic) in ideas" :key="topic">
                        <TableRow>
                            <TableCell :rowspan="idea.variations.length" class="text-sm font-medium">
                                {{ topic }}
                            </TableCell>
                            <TableCell class="text-sm">{{ idea.variations[0].variation }}</TableCell>
                            <TableCell class="text-sm">{{ idea.variations[0].clickbait_title }}</TableCell>
                        </TableRow>
                        <TableRow v-for="(variation, varIndex) in idea.variations.slice(1)" :key="varIndex">
                            <TableCell class="text-sm">{{ variation.variation }}</TableCell>
                            <TableCell class="text-sm">{{ variation.clickbait_title }}</TableCell>
                        </TableRow>
                    </template>
                </TableBody>
            </Table>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import jsonAutocomplete from 'json-autocomplete';

import LoadingTable from '@/components/LoadingTable.vue';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

const topic = ref('');
const additionalInstructions = ref('');
const ideas = ref({});
const isLoading = ref(false);

const generateIdeas = async () => {
    isLoading.value = true;
    const token = localStorage.getItem('token');

    console.log('Starting to generate ideas...');
    console.log('Topic:', topic.value);
    console.log('Additional Instructions:', additionalInstructions.value);

    try {
        const response = await fetch('http://127.0.0.1:5000/api/generate_content_ideas', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                topic: topic.value,
                additional_instructions: additionalInstructions.value,
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

            //console.log('Received chunk:', decoder.decode(value));
            //console.log('Current JSON Response:', jsonResponse);

            try {
                const completeJsonString = jsonAutocomplete(jsonResponse);
                let parsedJson = completeJsonString;

                parsedJson = parsedJson.replace(/json/g, '');
                parsedJson = parsedJson.replace('```', '');

                parsedJson = JSON.parse(parsedJson);

                console.log(parsedJson);


            } catch (error) {
                console.error('Error parsing JSON:', error);
            }
        }
    } catch (error) {
        console.error('Error fetching ideas:', error);
    } finally {
        isLoading.value = false;
        console.log('Finished generating ideas.');
    }
};
</script>