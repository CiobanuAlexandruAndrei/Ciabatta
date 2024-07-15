<template>
    <div class="flex gap-4 mt-12 mb-12">

        <div v-if="keywords.length > 0">
            <ul v-for="item in keywords" :key="item">
                <li> {{ item }} </li>
            </ul>
        </div>  
        
        <div v-else>
            No saved keywords
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const keywords = ref({});


onMounted(async () => {
    getSavedKeywords();
});

const getSavedKeywords = async () => {
    const token = localStorage.getItem("token");
    try {
        const response = await axios.get(
            "http://127.0.0.1:8000/api/get-keywords",
            {
                headers: {
                    Authorization: `Token ${token}`

                },
            }
        );
        keywords.value = response.data.keywords;
        console.log('SAVEDDD')
        console.log(response.data)
    } catch (error) {
        console.error("Error searching keyword:", error);
    }
};


</script>
