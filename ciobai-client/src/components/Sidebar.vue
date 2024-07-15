<template>
  <div :class="['flex flex-col h-screen transition-width duration-300 border-r-2 border-black', isCollapsed ? 'w-20' : 'w-64']">
    <div class="flex items-center justify-between p-4 border-b">
      <h1 class="text-xl font-bold" v-if="!isCollapsed">Tiseo</h1>
      <button @click="toggleCollapse" aria-label="Toggle Sidebar">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="isCollapsed ? 'M4 6h16M4 12h16M4 18h16' : 'M4 6h16M4 12h16M4 18h16'"/>
        </svg>
      </button>
    </div>
    <nav class="flex-1 px-2 py-4 space-y-1">
      <div v-for="item in menuItems" :key="item.label">
        <router-link 
          :to="item.route" 
          class="w-full flex items-center p-2 text-base font-medium rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <img :src="item.icon" alt="icon" class="w-6 h-6 mr-3" />
          <span v-if="!isCollapsed">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>
    <div class="p-4 border-t mt-auto flex flex-col items-center lg:flex-row lg:justify-between">
      <router-link 
        to="/logout" 
        class="flex items-center text-base font-medium rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        aria-label="Logout"
      >
        <img src="@/assets/img/logout_icon.png" alt="Logout" class="w-6 h-6" />
        <span v-if="!isCollapsed" class="ml-2">Logout</span>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

// Importing images
import dashboardIcon from '@/assets/img/charts_icon.png'
import keywordsIcon from '@/assets/img/keyword_icon.png'
import settingsIcon from '@/assets/img/settings_icon.png'
import logoutIcon from '@/assets/img/logout_icon.png'

interface MenuItem {
  label: string
  route: string
  icon: string
}

const menuItems: MenuItem[] = [
  { label: 'Dashboard', route: '/', icon: dashboardIcon },
  { label: 'Keywords', route: '/keywords', icon: keywordsIcon },
]

const isCollapsed = ref(false)
const router = useRouter()

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const handleResize = () => {
  if (window.innerWidth < 1000) { // Adjust this value based on your desired breakpoint
    isCollapsed.value = true
  } else {
    isCollapsed.value = false
  }
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* You can add additional styles here if needed */
</style>