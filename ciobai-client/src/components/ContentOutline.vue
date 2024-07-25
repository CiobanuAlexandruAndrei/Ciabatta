<template>
    <div class="w-full">

        <div class="w-full">
            <div v-if="contentOutline.content_outline">
                {{ contentOutline.content_outline.content.title }}
                <br>
                <br>
                {{ contentOutline.content_outline.content.target_audience }}
                <br>
                <br>
                {{ contentOutline.content_outline.content.wrote_as }}
                <br>
                <br>
                {{ contentOutline.content_outline.content.content }}
                <br>
                <br>
                <hr>
                <br>
                URL: {{ contentOutline.content_outline.content.metatags.url }}
                <br>
                <br>
                Page Title: {{ contentOutline.content_outline.content.metatags.page_title }}
                <br>
                <br>
                Page Description: {{ contentOutline.content_outline.content.metatags.page_description }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import jsonAutocomplete from 'json-autocomplete';

const router = useRouter();
const props = defineProps(['contentOutlineId']);

const contentOutlineId = ref('');
const contentOutline = ref({});

async function fetchContentOutline() {
    const token = localStorage.getItem('token');

    console.log('Starting to fetch content outline...');
    console.log('Content Outline ID:', contentOutlineId.value);

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/get_content_outline/${contentOutlineId.value}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.body) {
            throw new Error('ReadableStream not yet supported in this browser.');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            try {
             
                // const updatedOutline = JSON.parse(buffer);
                // contentOutline.value = updatedOutline;
                // console.log('Updated content outline:', updatedOutline);

                console.log(buffer)
                let updatedOutline = jsonAutocomplete(buffer);
                
                updatedOutline = updatedOutline.replace(/json/g, '');
                updatedOutline = updatedOutline.replace('```', '');
                updatedOutline = updatedOutline.replaceAll('\n', '')

                updatedOutline = JSON.parse(updatedOutline);

                contentOutline.value = updatedOutline;
                console.log(contentOutline.value)
            } catch (error) {
                console.log(error)
                console.log('Incomplete JSON, buffering...');
            }
        }
    } catch (error) {
        console.error('Error fetching content outline:', error);
    } finally {
        console.log('Finished fetching content outline.');
    }
}

onMounted(() => {
    const routeParams = router.currentRoute.value.params;
    contentOutlineId.value = routeParams.id;
    fetchContentOutline();
});
</script>