<template>
    <Toaster />
    <DropdownMenu :open="restOpen" @update:open="setNotVisible">
        <DropdownMenuTrigger> 
            <Button :class="buttonClasses">
                <div v-if="variant == 'copy'" class="h-full">
                    <img src="@/assets/img/copy_icon.png" class="h-full opacity-70" />
                </div>
                <div v-if="variant == 'save'" class="h-full">
                    <img src="@/assets/img/save_icon.png" class="h-full opacity-70" />
                </div>
                {{ buttonText }} 
            </Button> 
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-[200px]">
            <DropdownMenuLabel> Save to cluster </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <CreateKeywordClusterBtn @clusterCreated="handleClusterCreated" />
            <div class="p-1">
                <RadioGroup class="my-3" v-model="selectedClusterId">
                <div v-for="cluster in keywordClusters" :key="cluster.id">
                    <div class="flex items-center space-x-2">
                        <RadioGroupItem :value="cluster.id" :id="cluster.id"
                            @click="selectedClusterId = cluster.id" />
                        <Label :htmlFor="cluster.id"> {{ cluster.name }} </Label>
                    </div>
                </div>
            </RadioGroup>
            </div>
            <Button type="submit" class="p-1 text-xs h-8 w-full" @click="addKeywordToCluster()"> Save </Button>
        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import axios from "axios";
import { Toaster } from '@/components/ui/toast';
import { Button } from "@/components/ui/button";
import CreateKeywordClusterBtn from '@/components/CreateKeywordClusterBtn.vue';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useToast } from '@/components/ui/toast/use-toast';
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

const props = defineProps(['keyword', 'keywordClusters', 'buttonClasses', 'buttonText', 'variant']);
const selectedClusterId = ref("");
const showSelectClusterAlert = ref(false);
const restOpen = ref(false);
const emit = defineEmits(['clusterCreated']);
const { toast } = useToast();

const addKeywordToCluster = async () => {
    console.log(selectedClusterId.value);
    console.log(props.keyword);

    if (!selectedClusterId.value) {
        showSelectClusterAlert.value = true;
        console.log('Please select a cluster.');
        return;
    }

    try {
        const token = localStorage.getItem("token");
        const response = await axios.post("http://127.0.0.1:5000/api/add_keyword_to_cluster", {
            keyword_name: props.keyword,
            cluster_id: selectedClusterId.value
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        if (response.status === 201) {
            console.log('Keyword added to cluster successfully');
            restOpen.value = false;
            toast({
                class: 'top-0 right-0 flex fixed md:max-w-[420px] md:top-4 md:right-4 shadow-none text-green-600',
                description: 'Success, Keyword added to cluster successfully!',
            });

            // Optionally, you can add some UI feedback here
        } else {
            console.error('Error adding keyword to cluster:', response.data.message);
        }
    } catch (error) {
        console.error("Error adding keyword to cluster:", error);
    }
}

const handleClusterCreated = () => {
    emit("clusterCreated");
};

const setNotVisible = () => {
    restOpen.value = !restOpen.value;
}

</script>