<template>
    <div class="mt-12 mb-3 relative">
        <div class="flex flex-wrap gap-3 w-full mb-12">
            <Input v-model="topic" type="text" placeholder="Keyword or Topic" class="w-[300px]" />
            <Input v-model="additionalInstructions" placeholder="Additional Instructions" class="w-full" />
            <Button @click="generateIdeas" variant="secondary">
                Search
            </Button>
        </div>

        <div class="mt-8">
            <Table class="mt-3 w-full">
                <TableHeader>
                    <TableRow>
                        <TableHead>Semantically Related Topic</TableHead>
                        <TableHead>Variations on the Topic</TableHead>
                        <TableHead>Clickbait Style Title</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <template v-for="(topic, topicIndex) in ideas.topics" :key="topicIndex">
                        <TableRow v-if="topic.unique_semantically_related_topic">
                            <TableCell :rowspan="topic.variations.length" class="text-sm font-medium">
                                {{ topic.unique_semantically_related_topic }}
                            </TableCell>
                            <TableCell v-if="topic.variations[0]?.variation" class="text-sm">{{ topic.variations[0].variation }}</TableCell>
                            <TableCell v-if="topic.variations[0]?.clickbait_title" class="text-sm">{{ topic.variations[0].clickbait_title }}</TableCell>
                        </TableRow>
                        <TableRow v-for="(variation, varIndex) in topic.variations.slice(1)" :key="varIndex">
                            <TableCell v-if="variation.variation" class="text-sm">{{ variation.variation }}</TableCell>
                            <TableCell v-if="variation.clickbait_title" class="text-sm">{{ variation.clickbait_title }}</TableCell>
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
const ideas = ref({ topics: [] });

const generateIdeas = async () => {
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

            try {
                const completeJsonString = jsonAutocomplete(jsonResponse);
                let parsedJson = completeJsonString;

                parsedJson = parsedJson.replace(/json/g, '');
                parsedJson = parsedJson.replace('```', '');

            
                parsedJson = JSON.parse(parsedJson);
                ideas.value = parsedJson;
                console.log(parsedJson);
            } catch (error) {
                //console.error('Error parsing JSON:', error);
            }
        }
    } catch (error) {
        console.error('Error fetching ideas:', error);
    } finally {
        console.log('Finished generating ideas.');
    }
};
</script>