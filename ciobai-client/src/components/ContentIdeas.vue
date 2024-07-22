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

        <div v-if="ideas.length > 0" class="mt-8">
            <Table class="mt-3 w-full">
                <TableHeader>
                    <TableRow>
                        <TableHead>Semantically Related Topic</TableHead>
                        <TableHead>Variations on the Topic</TableHead>
                        <TableHead>Clickbait Style Title</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <template v-for="(idea, index) in ideas" :key="index">
                        <TableRow>
                            <TableCell :rowspan="idea.variations.length" class="text-sm font-medium">
                                {{ idea.unique_semantically_related_topic }}
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
import axios from 'axios';

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
const ideas = ref([]);
const isLoading = ref(false);

const generateIdeas = async () => {
    isLoading.value = true;
    const token = localStorage.getItem('token');
    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/api/generate_content_ideas',
            {
                topic: topic.value,
                additional_instructions: additionalInstructions.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }
        );

        if (response.data && response.data.result) {
            ideas.value = response.data.result.topics.map(topic => ({
                unique_semantically_related_topic: topic.unique_semantically_related_topic,
                variations: topic.variations.map(variation => ({
                    variation: variation.variation,
                    clickbait_title: variation.clickbait_title
                }))
            }));
        }
    } catch (error) {
        console.error('Error generating keywords:', error);
    } finally {
        isLoading.value = false;
    }
}
</script>