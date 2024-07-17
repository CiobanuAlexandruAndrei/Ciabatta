<template>
    <Dialog :open="restOpen" @update:open="setNotVisible">
      <DialogTrigger class="w-full">
        <Button variant="outline" class="w-full text-xs h-8">Create</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create Keywords Cluster</DialogTitle>
        </DialogHeader>
        <Input v-model="clusterName" class="mt-2" placeholder="Cluster name" />
        
        <DialogFooter class="w-full">
            <Button type="submit" @click="createCluster" class="mt-4 w-full">Save</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </template>

<script setup>
import { ref } from 'vue';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import axios from 'axios';
import DialogFooter from './ui/dialog/DialogFooter.vue';

const clusterName = ref('');
const restOpen = ref(false);
const emit = defineEmits(['clusterCreated']);

const createCluster = async () => {
  if (clusterName.value.trim() === '') {
    alert('Cluster name is required');
    return;
  }
  const token = localStorage.getItem("token");
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/create-keyword-cluster', {
        keyword_cluster_name: clusterName.value,
    }, {
      headers: {
        Authorization: `Token ${token}`,
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
</script>