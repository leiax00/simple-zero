import { createRouter, createWebHistory, Router } from 'vue-router'
import { routes } from '@/router/routes'

const router: Router = createRouter({
  history: createWebHistory(import.meta.env.VITE_APP_PREFIX),
  routes
})

router.beforeEach(async (to, from, next) => {
  next()
})

router.afterEach(() => {
})

export default router
