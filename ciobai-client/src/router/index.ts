import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import KeywordsView from '@/views/KeywordsView.vue'
import ContentGenerationView from '@/views/ContentGenerationView.vue'
import SavedContentIdeasView from '@/views/SavedContentIdeasView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/keywords',
      name: 'keywords',
      component: KeywordsView
    },
    {
      path: '/content-generation',
      name: 'content',
      component: ContentGenerationView
    },
    {
      path: '/saved-content-ideas',
      name: 'saved-content-ideas',
      component: SavedContentIdeasView
    },
  ]
})

export default router
