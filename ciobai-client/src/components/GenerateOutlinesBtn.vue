<template>
    <Dialog :open="restOpen" @update:open="setNotVisible">
        <DialogTrigger class="">
            <Button class="">
                <img src="@/assets/img/next_icon.png" class="h-full" />
            </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Generate Post Outline</DialogTitle>
            </DialogHeader>

            <Input v-model="postTitle" class="mt-2" placeholder="Post Title" />

            <div class="flex gap-2">
                <Input v-model="targetAudience" class="" placeholder="Target Audience" />
                <Button variant="outline">
                    <img src="@/assets/img/ai_icon.png" class="h-full opacity-60" />
                </Button>
            </div>

            <div class="flex gap-2">
                <Input v-model="wroteAs" class="" placeholder="Wrote As" />
                <Button variant="outline">
                    <img src="@/assets/img/ai_icon.png" class="h-full opacity-60" />
                </Button>
            </div>

            <Input v-model="additionalInfo" class="" placeholder="Additional Info" />

            <div class="flex gap-2 px-1 my-3">
                <Checkbox id="deleteContentIdea" v-model="deleteContentIdea" />
                <label for="deleteContentIdea"
                    class="text-sm leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Delete Content Idea
                </label>
            </div>

            <DialogFooter class="w-full">
                <Button type="submit" @click="createContentOutlineTask" class="mt-4 w-full">Save</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from '@/components/ui/checkbox';
import DialogFooter from './ui/dialog/DialogFooter.vue';

const postTitle = ref('');
const targetAudience = ref('');
const wroteAs = ref('');
const additionalInfo = ref('');
const deleteContentIdea = ref(false);
const restOpen = ref(false);
const emit = defineEmits(['contentOutlineCreated']);
const props = defineProps(['contentIdeaId', 'importedPostTitle']);

const createContentOutlineTask = async () => {
    if (postTitle.value.trim() === '') {
        alert('Post Title is required');
        return;
    }

    const token = localStorage.getItem("token");

    try {
        const response = await axios.post('http://127.0.0.1:5000/api/create_content_outline_task', {
            title: postTitle.value,
            target_audience: targetAudience.value,
            wrote_as: wroteAs.value,
            additional_info: additionalInfo.value,
            content_idea_id: props.contentIdeaId,
            delete_content_idea: deleteContentIdea.value,
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        if (response.status === 200) { 
            postTitle.value = '';
            targetAudience.value = '';
            wroteAs.value = '';
            additionalInfo.value = '';
            deleteContentIdea.value = false;
            restOpen.value = false;
            emit('contentOutlineCreated');
        }
    } catch (error) {
        console.error('Error creating content outline task:', error);
    }
};

const setNotVisible = () => {
    restOpen.value = !restOpen.value;
}

onMounted(() => {
    if (props.importedPostTitle) {
        postTitle.value = props.importedPostTitle;
    }
});
</script>