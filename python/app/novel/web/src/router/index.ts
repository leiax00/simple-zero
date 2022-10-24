import { createRouter, createWebHashHistory, Router } from 'vue-router'
import { routes } from '@/router/routes'

const router: Router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  next()
})

router.afterEach(() => {
})

export default router
