<template>
    <Dialog :open="restOpen" @update:open="setNotVisible">
        <DialogTrigger>
            <Button variant="outline" class="h-[25px] flex gap-3 items-center text-xs">
                <img class="h-[15px]" src="@/assets/img/edit_icon.png" />
                Edit Cluster Name
            </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Edit Keywords Cluster Name</DialogTitle>
            </DialogHeader>
            <Input v-model="clusterName" class="mt-2" placeholder="Cluster name" @keyup.enter="updateClusterName" />
            <DialogFooter class="w-full">
                <Button type="submit" @click="updateClusterName" class="mt-4 w-full">Save</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref } from 'vue';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import axios from 'axios';

const props = defineProps({
    cluster: Object,
});
const emit = defineEmits(['clusterUpdated']);

const restOpen = ref(false);
const clusterName = ref(props.cluster.name);

const updateClusterName = async () => {
    if (clusterName.value.trim() === '') {
        alert('Cluster name is required');
        return;
    }
    const token = localStorage.getItem("token");
    try {
        const response = await axios.put('http://127.0.0.1:5000/api/update_keyword_cluster_name', {
            keyword_cluster_id: props.cluster.id,
            keyword_cluster_name: clusterName.value,
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });
        if (response.status === 200) {
            emit('clusterUpdated');
            restOpen.value = false;
        }
    } catch (error) {
        console.error('Error updating keyword cluster name:', error);
    }
};

const setNotVisible = () => {
    restOpen.value = !restOpen.value;
};
</script>