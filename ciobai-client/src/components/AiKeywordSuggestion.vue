<template>
    <div class="flex gap-4 mt-12 mb-4">
        <Input v-model="topicName" placeholder="Topic or Keyword" />
    
        <Select v-model="intentName">
            <SelectTrigger>
            <SelectValue placeholder="Intent" />
            </SelectTrigger>
            <SelectContent>
            <SelectGroup>
                <SelectItem value="informational">
                Informational
                </SelectItem>
                <SelectItem value="commercial">
                Commercial
                </SelectItem>
            </SelectGroup>
            </SelectContent>
        </Select>
    </div>
    <div>
        <Input v-model="additionaInstructions" placeholder="Additional Instructions" />
        <Button @click="generateKeywords()" variant="secondary" class="mt-4">Generate</Button>
    </div>
    <div v-if="isLoading" class="mt-5">
        <LoadingTable />
    </div>
    <div v-if="keywords.length > 0 && !isLoading" class="mt-5">
        <Table>
            <TableHeader>
            <TableRow>
                <TableHead>
                Name
                </TableHead>
                <TableHead class="text-right">
                    Action
                </TableHead>
            </TableRow>
            </TableHeader>
            <TableBody>
            <TableRow v-for="item in keywords" :key="item">
                <TableCell class="text-sm">
                {{ item }}
                </TableCell>
                
                <TableCell class="">
                    <div class="flex justify-end gap-1">
                        <Button variant="outline">test</Button>
                        <SaveToKeywordcluster :keyword="item" />
                    </div>
                </TableCell>
            </TableRow>
            </TableBody>
        </Table>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import SaveToKeywordcluster from '@/components/SaveToKeywordCluster.vue'
import LoadingTable from '@/components/LoadingTable.vue'

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

const topicName = ref("");
const intentName = ref("");
const additionaInstructions = ref("");
const keywords = ref([]);
const isLoading = ref(false);

const generateKeywords = async () => {
    isLoading.value = true;
    const token = localStorage.getItem("token");
    try {
        console.log(topicName.value);
        console.log(intentName.value);
        console.log(additionaInstructions.value);

        const response = await axios.post(
            "http://127.0.0.1:8000/api/generate-keyword-suggestions",
            {
                topic: topicName.value,
                intent: intentName.value,
                additional_instructions: additionaInstructions.value,
            },
            {
                headers: {
                    Authorization: `Token ${token}`,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );

        keywords.value = response.data.result.keywords;
        console.log(keywords.value)
        isLoading.value = false;

    } catch (error) {
        console.error("Error generating keyword:", error);
    }
};
</script>