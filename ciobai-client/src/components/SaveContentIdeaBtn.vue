<template>
    <div>
        <Button v-if="!isSaved" @click="createContentIdea" class="bg-green-300 text-black text-sm hover:bg-green-400">
            <img src="@/assets/img/save_icon.png" class="h-full opacity-70" />
        </Button>
        <Button variant="ghost" v-else>
            <img src="@/assets/img/ok_icon.png" class="h-full" />
        </Button>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';
import axios from 'axios';
import { Button } from '@/components/ui/button';

const props = defineProps({
    title: String,
    topicVariation: String,
    topicCategory: String
});

const isSaved = ref(false);

const checkIfSaved = async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await axios.post('http://127.0.0.1:5000/api/check_content_idea', 
            {
                title: props.title,
                topic_variation: props.topicVariation,
                topic_category: props.topicCategory
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                }
            }
        );
        isSaved.value = response.data.is_saved;
    } catch (error) {
        console.error(error);
    }
};

const createContentIdea = async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await axios.post('http://127.0.0.1:5000/api/create_content_idea', 
            {
                title: props.title,
                topic_variation: props.topicVariation,
                topic_category: props.topicCategory
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                }
            }
        );
        console.log(response.data);
        isSaved.value = true;
    } catch (error) {
        console.error(error);
    }
};

onMounted(async () => {
    await checkIfSaved();
});
</script>