<template>
    <div v-for="index in 10" :key="index">
        <Skeleton class="h-[40px] w-full mb-5" />
    </div>
    
</template>

<script setup>
import { Skeleton } from '@/components/ui/skeleton'
</script>