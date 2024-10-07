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
            <div class="relative w-full max-w-sm">
                <TagsInput v-model="modelValue" class="w-[300px] p-1">
                    <div class="flex gap-2 flex-wrap items-center max-w-full break-words">
                        <TagsInputItem v-for="item in modelValue" :key="item" :value="item" class="max-w-full min-w-[50px] h-auto break-words">
                            <TagsInputItemText class="max-w-[93%] h-auto"/>
                            <TagsInputItemDelete />
                        </TagsInputItem>
                    </div>
                    <ComboboxRoot v-model="modelValue" v-model:open="open" v-model:searchTerm="searchTerm" class="w-full bg-white">
                        <ComboboxAnchor as-child>
                            <ComboboxInput placeholder="Keyword or Topic..." as-child>
                                <TagsInputInput ref="tagsInput" class="w-full px-3" :class="modelValue.length > 0 ? 'mt-2' : ''" @keydown.enter.prevent="addNewKeyword" />
                            </ComboboxInput>
                        </ComboboxAnchor>
                        <ComboboxPortal class="p-1">
                            <CommandList
                                position="popper"
                                class="w-full rounded-md mt-2 border bg-popover text-popover-foreground shadow-md outline-none z-10 bg-white"
                            >
                                <CommandEmpty class="w-full p-0">
                                    <div class="p-2 w-full">
                                        Click Enter To Add
                                    </div>
                                </CommandEmpty>
                                <CommandGroup>
                                    <CommandItem v-for="keyword in filteredKeywords" class="flex gap-2 justify-between" :key="keyword.name" :value="keyword.name" @select.prevent="addKeyword(keyword.name)">
                                        <div>{{ keyword.name }}</div>
                                        <div class="text-xs text-gray-500 ml-2">{{ keyword.cluster }}</div>
                                    </CommandItem>
                                </CommandGroup>
                            </CommandList>
                        </ComboboxPortal>
                    </ComboboxRoot>
                </TagsInput>
            </div>
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
                                <TableCell v-if="varIndex === 0" :rowspan="topic.variations.length" class="text-sm font-medium">
                                    {{ topic.unique_semantically_related_topic }}
                                </TableCell>
                                <TableCell v-if="variation.variation" class="text-sm">{{ variation.variation }}</TableCell>
                                <TableCell v-if="variation.clickbait_title" class="text-sm">{{ variation.clickbait_title }}</TableCell>
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
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useContentIdeasStore } from '@/store/contentIdeas';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import axios from "axios";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import { ComboboxAnchor, ComboboxInput, ComboboxPortal, ComboboxRoot } from 'radix-vue';
import { CommandEmpty, CommandGroup, CommandItem, CommandList } from '@/components/ui/command';
import { TagsInput, TagsInputInput, TagsInputItem, TagsInputItemDelete, TagsInputItemText } from '@/components/ui/tags-input';
import SaveContentIdeaBtn from '@/components/SaveContentIdeaBtn.vue';
import SavedContentIdeas from '@/components/SavedContentIdeas.vue';

const router = useRouter();
const store = useContentIdeasStore();

const topic = ref(store.topic);
const additionalInstructions = ref(store.additionalInstructions);
const ideas = ref(store.ideas);

const keywordClusters = ref([]);
const clusters = ref([]); // Store all keywords
const modelValue = ref([]);
const open = ref(false);
const searchTerm = ref("");

const tagsInput = ref(null);

const fetchKeywordClusters = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/api/get_keywords_clusters", {
            headers: {
                Authorization: `Bearer ${token}`
            },
        });
        keywordClusters.value = response.data.clusters;
        clusters.value = keywordClusters.value.flatMap(cluster => cluster.keywords.map(keyword => ({ name: keyword.name, cluster: cluster.name })));
    } catch (error) {
        console.error("Error fetching keywords clusters:", error);
    }
};

const filteredKeywords = computed(() => {
    const keywords = clusters.value.filter(keyword => !modelValue.value.includes(keyword.name));
    if (searchTerm.value && !keywords.some(keyword => keyword.name === searchTerm.value)) {
        keywords.unshift({ name: searchTerm.value, cluster: '' });
    }
    return keywords;
});

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
    store.setTopic(modelValue.value.join(", "));
    store.setAdditionalInstructions(additionalInstructions.value);
    store.generateIdeas();
};

const addKeyword = (keyword) => {
    closeCombobox();
    modelValue.value.push(keyword);
    searchTerm.value = '';

};

const addNewKeyword = () => {
    if (searchTerm.value && !modelValue.value.includes(searchTerm.value)) {
        modelValue.value.push(searchTerm.value);
        searchTerm.value = '';
        closeCombobox(); // Close combobox after adding a new keyword

    }
};

const closeCombobox = () => {
    open.value = false;
};



onMounted(async () => {
    await fetchKeywordClusters();
});
</script>