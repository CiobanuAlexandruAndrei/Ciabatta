<template>

</template>

<script setup>
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';



const router = useRouter();

localStorage.removeItem('token');
router.push('/login');

</script>