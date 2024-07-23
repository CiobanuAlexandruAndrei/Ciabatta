<template>
    <div class="mt-8">
        <div v-if="selectedIdeas.length > 0" class="w-full flex justify-end gap-2 h-[60px]">
            <Button class="flex gap-2">
                <img src="@/assets/img/next_icon.png" class="h-full block" />
                <div>
                    Generate Content Outlines
                </div>
            </Button>
            <AlertDialog>
                <AlertDialogTrigger as-child>
                    <Button variant="destructive" class="flex gap-2">
                        <img class="h-[15px]" src="@/assets/img/trash_icon.png" />
                        <div>
                            Delete Selected
                        </div>
                    </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                            This action cannot be undone. This will permanently delete the selected content ideas.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction @click="deleteSelectedIdeas">Delete</AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </div>
        <div v-else class="h-[60px]"></div> <!-- The table doesn't move when selecting ideas -->
        <div class="flex justify-between items-center mb-4">
            <div class="relative w-full max-w-sm items-center">
                <Input
                    id="search"
                    type="text"
                    v-model="searchTerm"
                    placeholder="Search saved content ideas..."
                    autocomplete="off"
                    class="pl-10"
                />
                <span class="absolute start-0 inset-y-0 flex items-center justify-center px-2">
                    <img src="@/assets/img/search_icon.png" class="h-6 w-6 text-muted-foreground opacity-60" />
                </span>
            </div>
            <div class="mr-4 text-sm text-gray-600 flex gap-4">
                <div v-if="selectedIdeas.length > 0">
                    Selected: {{ selectedIdeas.length }} 
                </div>

                <div>
                    Results: {{ filteredContentIdeas.length }}
                </div>

            </div>
        </div>

        <Table class="my-3 w-full">
            <TableHeader>
                <TableRow>
                    <TableCell>
                        <Checkbox id="selectAll" :checked="allSelected" @click="toggleSelectAll" />
                    </TableCell>
                    <TableCell>Title</TableCell>
                    <TableCell>Topic Variation</TableCell>
                    <TableCell>Main Topic</TableCell>
                    <TableCell>Actions</TableCell>
                </TableRow>
            </TableHeader>
            <TableBody>
                <TableRow v-for="idea in filteredContentIdeas" :key="idea.id">
                    <TableCell class="text-sm max-w-[400px]">
                        <Checkbox :id="`idea-${idea.id}`" :checked="selectedIdeas.includes(idea.id)"
                            @click="() => toggleSelection(idea.id)" />
                    </TableCell>
                    <TableCell class="text-sm max-w-[700px]">{{ idea.title }}</TableCell>
                    <TableCell class="text-sm">{{ idea.topic_variation }}</TableCell>
                    <TableCell class="text-sm">{{ idea.topic_category }}</TableCell>
                    <TableCell class="text-sm text-right">
                        <AlertDialog>
                            <AlertDialogTrigger as-child>
                                <Button variant="destructive" @click="() => confirmDeleteIdea(idea.id)">
                                    <img class="h-[15px]" src="@/assets/img/trash_icon.png" />
                                </Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent>
                                <AlertDialogHeader>
                                    <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                                    <AlertDialogDescription>
                                        This action cannot be undone. This will permanently delete the content idea.
                                    </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                                    <AlertDialogAction @click="deleteIdea">Delete</AlertDialogAction>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialog>
                    </TableCell>
                </TableRow>
            </TableBody>
        </Table>
        <div v-if="filteredContentIdeas.length == 0" class="py-4 text-center w-full text-sm">
            No results found
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from '@/components/ui/alert-dialog';

import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

const contentIdeas = ref([]);
const selectedIdeas = ref([]);
const searchTerm = ref("");
const ideaToDelete = ref(null);

const fetchContentIdeas = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/api/get_content_ideas", {
            headers: {
                Authorization: `Bearer ${token}`
            },
        });
        contentIdeas.value = response.data.result;
        console.log(contentIdeas.value);
    } catch (error) {
        console.error("Error fetching content ideas:", error);
    }
};

const toggleSelection = (id) => {
    if (selectedIdeas.value.includes(id)) {
        selectedIdeas.value = selectedIdeas.value.filter(ideaId => ideaId !== id);
    } else {
        selectedIdeas.value.push(id);
    }
};

const toggleSelectAll = () => {
    if (allSelected.value) {
        selectedIdeas.value = [];
    } else {
        selectedIdeas.value = contentIdeas.value.map(idea => idea.id);
    }
};

const allSelected = computed(() => {
    return selectedIdeas.value.length === contentIdeas.value.length;
});

const filteredContentIdeas = computed(() => {
    if (!searchTerm.value) {
        return contentIdeas.value;
    }
    return contentIdeas.value.filter(idea => 
        idea.title.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
        idea.topic_variation.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
        idea.topic_category.toLowerCase().includes(searchTerm.value.toLowerCase())
    );
});

const deleteSelectedIdeas = async () => {
    try {
        const token = localStorage.getItem("token");
        for (const id of selectedIdeas.value) {
            await axios.delete("http://127.0.0.1:5000/api/delete_content_idea", {
                headers: {
                    Authorization: `Bearer ${token}`
                },
                data: { id }
            });
        }
        fetchContentIdeas();
        selectedIdeas.value = [];
    } catch (error) {
        console.error("Error deleting content ideas:", error);
    }
};

const confirmDeleteIdea = (id) => {
    ideaToDelete.value = id;
};

const deleteIdea = async () => {
    try {
        const token = localStorage.getItem("token");
        await axios.delete("http://127.0.0.1:5000/api/delete_content_idea", {
            headers: {
                Authorization: `Bearer ${token}`
            },
            data: { id: ideaToDelete.value }
        });
        fetchContentIdeas();
        ideaToDelete.value = null;
    } catch (error) {
        console.error("Error deleting content idea:", error);
    }
};

onMounted(async () => {
    fetchContentIdeas();
});
</script>