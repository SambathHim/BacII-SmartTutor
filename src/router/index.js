import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/quiz', name: 'Quiz', component: () => import('../views/QuizView.vue') },
    { path: '/', name: 'Home', component: HomeView },
    { path: '/bot', name: 'Bot', component: () => import('../views/BotView.vue') },
    {
      path: '/pasttests',
      name: 'Past-Tests',
      component: () => import('../views/PastTestView.vue'),
    },
    {
      path: '/calculator',
      name: 'Calculator',
      component: () => import('../views/CalculatorView.vue'),
    },
    {
      path: '/about',
      name: 'About',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
})

export default router