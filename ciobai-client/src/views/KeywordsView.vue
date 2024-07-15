<template>
    <div class="flex">
      <Sidebar @toggle-collapse="handleSidebarToggle" class="bg-white" />
      <div :class="['flex-1 p-4 md:p-8 lg:p-16 transition-all duration-300', isSidebarCollapsed ? 'collapsed-sidebar' : 'expanded-sidebar']">
        <Tabs default-value="search" class="w-full">
          <TabsList class="grid w-full grid-cols-3">
            <TabsTrigger value="search">Search & Related</TabsTrigger>
            <TabsTrigger value="ai-suggestion">AI Keyword Suggestions</TabsTrigger>
            <TabsTrigger value="saved">Keywords Clusters</TabsTrigger>
          </TabsList>
          <TabsContent value="search">
            <KeywordsSearch />
          </TabsContent>
          <TabsContent value="ai-suggestion">
            AI Suggestions 
          </TabsContent>
          <TabsContent value="saved">
            <KeywordsSaved />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import Sidebar from '@/components/Sidebar.vue'
  import KeywordsSearch from '@/components/KeywordsSearch.vue'
  import KeywordsSaved from '@/components/KeywordsSaved.vue'
  import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
  } from '@/components/ui/tabs'
  
  const isSidebarCollapsed = ref(false)
  
  const handleSidebarToggle = (collapsed: boolean) => {
    isSidebarCollapsed.value = collapsed
  }
  </script>
  
  <style scoped>
  /* You can add additional styles here if needed */
  </style>