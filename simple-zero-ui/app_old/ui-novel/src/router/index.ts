import { createRouter, createWebHistory } from 'vue-router'
import type { Router } from 'vue-router'
import { routes } from '@/router/routes'

const router: Router = createRouter({
  history: createWebHistory('/novel'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  next()
})

// eslint-disable-next-line @typescript-eslint/no-empty-function
router.afterEach(() => {})

export default router
