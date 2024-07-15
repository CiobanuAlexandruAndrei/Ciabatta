<template>
    <div class="flex">
        <Sidebar />
        <div class="flex-1 p-16">
            <Tabs default-value="search" class="w-full">
                <TabsList class="grid w-full grid-cols-2" >
                    <TabsTrigger value="search">
                        Search
                    </TabsTrigger>
                    <TabsTrigger value="saved">
                        Saved Keywords
                    </TabsTrigger>
                </TabsList>
                <TabsContent value="search">
                    <KeywordsSearch />
                </TabsContent>
                <TabsContent value="saved">
                    <KeywordsSaved />
                </TabsContent>
            </Tabs>
        </div>
    </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue'
import KeywordsSearch from '@/components/KeywordsSearch.vue'
import KeywordsSaved from '@/components/KeywordsSaved.vue'

import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from '@/components/ui/tabs'


</script>