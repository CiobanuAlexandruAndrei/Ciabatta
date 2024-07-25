<template>
    <div class="mt-8">
        <div>
            <div v-for="task in contentOutlinesTasks" :key="task.id">
                <router-link :to="'/content-outline/' + task.id">{{ task.id }} - {{ task }}</router-link>
                <hr/>
            </div>
        </div>
        <!-- <Table class="my-3 w-full">
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
                    <TableCell class="text-sm flex gap-2 min-w-[150px]">
                        <GenerateOutlinesBtn :importedPostTitle="idea.title" :contentIdeaId="idea.id" />
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
        </div> -->
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from 'vue-router';

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




const router = useRouter();


const contentOutlinesTasks = ref([]);

const fetchContentOutlinesTasks = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/api/get_all_content_outlines_tasks", {
            headers: {
                Authorization: `Bearer ${token}`
            },
        });
        contentOutlinesTasks.value = response.data.result;
        console.log(contentOutlinesTasks.value);
    } catch (error) {
        console.error("Error fetching content outlines tasks:", error);
    }
};


onMounted(async () => {
    fetchContentOutlinesTasks();
});
</script>