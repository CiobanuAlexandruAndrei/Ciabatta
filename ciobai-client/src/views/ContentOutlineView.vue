<template>
    <div class="flex">
        <Sidebar @toggle-collapse="handleSidebarToggle" class="bg-white" />
        <div
            :class="['flex-1 p-4 md:p-8 lg:p-16 transition-all duration-300', isSidebarCollapsed ? 'collapsed-sidebar' : 'expanded-sidebar']">
            <div>
                <Button variant="outline" @click="router.back()"> 
                    <img src="@/assets/img/go_back_icon.png" class="h-full opacity-30"/>
                </Button>
            </div>
            
            <ContentOutline :contentOutlineId="contentOutlineId"/>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import ContentOutline from '@/components/ContentOutline.vue'
import { Button } from '@/components/ui/button'
import {useRouter} from 'vue-router';

const router = useRouter();
import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from '@/components/ui/tabs'

const isSidebarCollapsed = ref(false)
const contentOutlineId = ref('');

const handleSidebarToggle = (collapsed: boolean) => {
    isSidebarCollapsed.value = collapsed
}

onMounted(() => {
    const routeParams = router.currentRoute.value.params;
    contentOutlineId.value = routeParams.id;
})

</script>


