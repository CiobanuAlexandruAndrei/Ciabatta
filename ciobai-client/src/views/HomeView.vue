<template>
  <div class="flex">
    <Sidebar @toggle-collapse="handleSidebarToggle" class="bg-white" />
    <div :class="['flex-1 p-4 md:p-8 lg:p-16 transition-all duration-300', isSidebarCollapsed ? 'collapsed-sidebar' : 'expanded-sidebar']">
      Dashboard
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'


const isSidebarCollapsed = ref(false)

const handleSidebarToggle = (collapsed: boolean) => {
  isSidebarCollapsed.value = collapsed
}
</script>

<style scoped>
/* You can add additional styles here if needed */
</style>