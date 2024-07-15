<template>
  <RouterView class="max-h-full overflow-y-scroll" />
</template>


<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import Sidebar from "./components/Sidebar.vue";
import { useRouter, useRoute } from 'vue-router';
import { ref } from 'vue';


const router = useRouter();
const route = useRoute();

const token = localStorage.getItem('token');
if(!token){
  router.push('/login')
}



</script>