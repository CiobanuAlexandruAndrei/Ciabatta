<template>
    <div class="mt-12 mb-3 relative">
        <div class="mb-8">
            <Button class="flex gap-2 h-[35px] w-full" variant="outline" @click="router.push('/saved-content-ideas');">
                <img src="@/assets/img/storage_icon.png" class="h-full block opacity-70"/>
                <div>
                    Saved
                </div>
            </Button>
        </div>
        <div class="flex flex-wrap gap-3 w-full mb-12">
            <Input v-model="topic" type="text" placeholder="Keyword or Topic" class="w-[300px]" />
            <Input v-model="additionalInstructions" placeholder="Additional Instructions" class="w-full" />
            <Button @click="generateIdeas" variant="secondary">
                Generate
            </Button>
        </div>

        <div class="mt-8">
            <Table class="mt-3 w-full" v-if="ideas.topics.length > 0">
                <TableHeader>
                    <TableRow>
                        <TableHead>Topic Category</TableHead>
                        <TableHead>Topic Variations</TableHead>
                        <TableHead>Titles</TableHead>
                        <TableHead>Action</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <template v-for="(topic, topicIndex) in ideas.topics" :key="topicIndex">
                        <template v-for="(variation, varIndex) in topic.variations" :key="varIndex">
                            <TableRow :class="{ 'bg-gray-100': isOddRow(topicIndex, varIndex) }">
                                <TableCell v-if="varIndex === 0" :rowspan="topic.variations.length"
                                    class="text-sm font-medium">
                                    {{ topic.unique_semantically_related_topic }}
                                </TableCell>
                                <TableCell v-if="variation.variation" class="text-sm">{{ variation.variation }}
                                </TableCell>
                                <TableCell v-if="variation.clickbait_title" class="text-sm">{{ variation.clickbait_title}}</TableCell>
                                <TableCell v-if="variation.clickbait_title" class="text-sm flex justify-end gap-2 min-w-[150px]">
                                    <SaveContentIdeaBtn :title="variation.clickbait_title" :topicVariation="variation.variation" :topicCategory="topic.unique_semantically_related_topic" />
                                    <Button> <img src="@/assets/img/next_icon.png" class="h-full" /> </Button>
                                </TableCell>
                            </TableRow>
                        </template>
                    </template>
                </TableBody>
            </Table>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useContentIdeasStore } from '@/store/contentIdeas';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import SaveContentIdeaBtn from '@/components/SaveContentIdeaBtn.vue'
import SavedContentIdeas from '@/components/SavedContentIdeas.vue'
import {useRouter} from 'vue-router';

const router = useRouter();
const store = useContentIdeasStore();

const topic = ref(store.topic);
const additionalInstructions = ref(store.additionalInstructions);
const ideas = ref(store.ideas);

watch(() => store.topic, (newTopic) => {
    topic.value = newTopic;
});

watch(() => store.additionalInstructions, (newInstructions) => {
    additionalInstructions.value = newInstructions;
});

watch(() => store.ideas, (newIdeas) => {
    ideas.value = newIdeas;
});

const isOddRow = (topicIndex, varIndex) => {
    return (topicIndex * ideas.value.topics[0].variations.length + varIndex) % 2 === 1;
};

const generateIdeas = () => {
    store.setTopic(topic.value);
    store.setAdditionalInstructions(additionalInstructions.value);
    store.generateIdeas();
};
</script>

