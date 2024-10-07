<template>
    <div class="flex">
        <Sidebar @toggle-collapse="handleSidebarToggle" class="bg-white" />
        <div
            :class="['flex-1 p-4 md:p-8 lg:p-16 transition-all duration-300', isSidebarCollapsed ? 'collapsed-sidebar' : 'expanded-sidebar']">
            <Tabs default-value="ideas" class="w-full">
                <TabsList class="grid w-full grid-cols-3">
                    <TabsTrigger value="ideas" class="flex gap-2">
                        <div>
                            <img src="@/assets/img/idea_icon.png" class="h-[15px] opacity-60" />
                        </div>
                        <div>
                            Content Ideas
                        </div>
                    </TabsTrigger>
                    <TabsTrigger value="outlines" class="flex gap-2">
                        <div> <img src="@/assets/img/project_icon.png" class="h-[15px] opacity-60" /> </div>
                        <div> Content Outlines </div>
                    </TabsTrigger>
                    <TabsTrigger value="creation" class="flex gap-2">
                        <div> <img src="@/assets/img/pen_icon.png" class="h-[15px] opacity-60" /> </div>
                        <div> Content Creation </div>
                    </TabsTrigger>
                </TabsList>
                <TabsContent value="ideas">
                    <ContentIdeas />
                </TabsContent>
                <TabsContent value="outlines">
                    <ContentOutlines />
                </TabsContent>
                <TabsContent value="creation">
                    Creation
                </TabsContent>
            </Tabs>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import ContentIdeas from '@/components/ContentIdeas.vue'
import ContentOutlines from '@/components/ContentOutlines.vue'
import { Button } from '@/components/ui/button'

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