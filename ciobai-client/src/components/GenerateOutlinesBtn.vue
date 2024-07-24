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
                <Input v-model="clusterName" class="" placeholder="Target Audience (by default auto generated)"
                    @keyup.enter="createCluster" />
                <Button variant="outline">
                    <img src="@/assets/img/ai_icon.png" class="h-full opacity-60" />
                </Button>
            </div>

            <div class="flex gap-2">
                <Input v-model="clusterName" class="" placeholder="Wrote As (by default auto generated)"
                    @keyup.enter="createCluster" />
                <Button variant="outline">
                    <img src="@/assets/img/ai_icon.png" class="h-full opacity-60" />
                </Button>
            </div>

            <Input v-model="clusterName" class="" placeholder="Additional Info" @keyup.enter="createCluster" />

            <div class="flex gap-2 px-1 my-3">
                <Checkbox id="terms" />
                <label for="terms"
                    class="text-sm leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Delete Content Idea
                </label>
            </div>


            <DialogFooter class="w-full">
                <Button type="submit" @click="createCluster" class="mt-4 w-full">Save</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";

import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import axios from 'axios';
import DialogFooter from './ui/dialog/DialogFooter.vue';
import { Checkbox } from '@/components/ui/checkbox'

const clusterName = ref('');
const restOpen = ref(false);
const emit = defineEmits(['clusterCreated']);
const props = defineProps(['contentIdeaId', 'importedPostTitle']);
const postTitle = ref('');

const createCluster = async () => {
    if (clusterName.value.trim() === '') {
        alert('Cluster name is required');
        return;
    }
    const token = localStorage.getItem("token");
    try {
        const response = await axios.post('http://127.0.0.1:5000/api/create_keyword_cluster', {
            keyword_cluster_name: clusterName.value,
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });
        if (response.status === 201) {
            clusterName.value = '';
            restOpen.value = false
            emit('clusterCreated');
        }
    } catch (error) {
        console.error('Error creating keyword cluster:', error);
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