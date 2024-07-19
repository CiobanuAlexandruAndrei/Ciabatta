<template>
    <div class="gap-4 mt-12 mb-12">
        <div class="mb-10">
            <CreateKeywordClusterBtn @clusterCreated="handleClusterCreated" />
        </div>
        <div v-if="keywordClusters.length > 0" class="w-full">
            <Collapsible v-for="item in keywordClusters" :key="item.id" class="mb-3">
                <CollapsibleTrigger class="w-full">
                    <div class="border-2 border-gray-300 p-1 px-5 w-full text-left rounded-lg flex items-center">
                        <div> {{ item.name }} </div>
                        <div class="ml-auto flex gap-5 items-center">
                            <div class="text-xs">
                                <div v-if="item.keywords.length > 0">
                                    ({{ item.keywords.length }})
                                </div>
                                <div v-else>
                                    (empty)
                                </div>
                            </div>
                            <div>
                                <img src="@/assets/img/drop_icon.png" class="h-[20px] opacity-70" />
                            </div>
                        </div>
                    </div>
                </CollapsibleTrigger>
                <CollapsibleContent class="w-full">
                    <div class="pt-4 px-1">
                        <AlertDialog>
                            <AlertDialogTrigger as-child>
                                <Button variant="destructive" class="h-[25px] flex gap-3 items-center text-xs"
                                    @click="confirmDeleteCluster(item.id)">
                                    <img class="h-[15px]" src="@/assets/img/trash_icon.png" />
                                    Delete Cluster
                                </Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent>
                                <AlertDialogHeader>
                                    <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                                    <AlertDialogDescription>
                                        This action cannot be undone. This will permanently delete your
                                        cluster and remove your data from our servers.
                                    </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                                    <AlertDialogAction @click="deleteCluster">Delete</AlertDialogAction>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialog>
                    </div>
                    <div v-if="!item.keywords.length" class="px-3 pt-2">
                        No keywords stored
                    </div>
                    <Table class="my-5">
                        <TableHeader>
                        </TableHeader>
                        <TableBody>
                            <TableRow v-for="keyword in item.keywords" :key="keyword.id">
                                <TableCell class="text-sm">
                                    {{ keyword.name }}
                                </TableCell>
                                <TableCell class="flex justify-end gap-2">
                                    <TestKeywordsButton variant="one" :keywords="[keyword.name]" />
                                    <div>
                                        <SaveToKeywordcluster @clusterCreated="handleClusterCreated" variant="copy"
                                            buttonClasses="bg-green-300 text-black text-sm hover:bg-green-400"
                                            :keyword="keyword.name" :keywordClusters="keywordClusters" />
                                    </div>
                                    <AlertDialog>
                                        <AlertDialogTrigger as-child>
                                            <Button variant="destructive"
                                                @click="confirmDeleteKeyword(item.id, keyword.name)">
                                                <img class="h-[15px]" src="@/assets/img/trash_icon.png" />
                                            </Button>
                                        </AlertDialogTrigger>
                                        <AlertDialogContent>
                                            <AlertDialogHeader>
                                                <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                                                <AlertDialogDescription>
                                                    This will remove the keyword from the cluster
                                                </AlertDialogDescription>
                                            </AlertDialogHeader>
                                            <AlertDialogFooter>
                                                <AlertDialogCancel>Cancel</AlertDialogCancel>
                                                <AlertDialogAction @click="deleteKeyword">Delete</AlertDialogAction>
                                            </AlertDialogFooter>
                                        </AlertDialogContent>
                                    </AlertDialog>
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CollapsibleContent>
            </Collapsible>
        </div>
        <div v-else>
            No keyword clusters
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
} from '@/components/ui/collapsible'
import { Button } from '@/components/ui/button'
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
} from '@/components/ui/alert-dialog'
import CreateKeywordClusterBtn from '@/components/CreateKeywordClusterBtn.vue'
import SaveToKeywordCluster from "@/components/SaveToKeywordCluster.vue";
import TestKeywordsButton from '@/components/TestKeywordsButton.vue';

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'

import SaveToKeywordcluster from '@/components/SaveToKeywordCluster.vue'

const keywordClusters = ref([]);
const clusterToDelete = ref(null);
const keywordToDelete = ref({ clusterId: null, keywordName: null });

const fetchKeywordClusters = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/api/get_keywords_clusters",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                },
            });
        keywordClusters.value = response.data.clusters;
        console.log(keywordClusters.value);
    } catch (error) {
        console.error("Error fetching keywords clusters:", error);
    }
};

const handleClusterCreated = () => {
    fetchKeywordClusters();
};

const deleteKeyword = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.delete("http://127.0.0.1:5000/api/delete_keyword_from_cluster", {
            headers: {
                Authorization: `Bearer ${token}`
            },
            data: {
                cluster_id: keywordToDelete.value.clusterId,
                keyword_name: keywordToDelete.value.keywordName
            }
        });

        if (response.status === 200) {
            fetchKeywordClusters();
            console.log('Keyword deleted successfully');
        }
    } catch (error) {
        console.error("Error deleting keyword from cluster:", error);
    }
};

const confirmDeleteCluster = (clusterId) => {
    clusterToDelete.value = clusterId;
};

const deleteCluster = async () => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.delete("http://127.0.0.1:5000/api/delete_keyword_cluster", {
            headers: {
                Authorization: `Bearer ${token}`
            },
            data: {
                cluster_id: clusterToDelete.value
            }
        });

        if (response.status === 200) {
            fetchKeywordClusters();
            console.log('Cluster deleted successfully');
        }
    } catch (error) {
        console.error("Error deleting cluster:", error);
    }
};

const confirmDeleteKeyword = (clusterId, keywordName) => {
    keywordToDelete.value = { clusterId, keywordName };
};

onMounted(async () => {
    fetchKeywordClusters();
});
</script>
