import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  {
    path: '/events',
    name: 'events',
    component: () => import('../views/EventsView.vue'),
  },
  {
    path: '/event/:id',
    name: 'event',
    component: () => import('../views/EventView.vue'),
    props: true,
  },
  {
    path: '/fight/:id',
    name: 'fight',
    component: () => import('../views/FightView.vue'),
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
