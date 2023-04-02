import { createRouter, createWebHistory } from 'vue-router'
import type { Router } from 'vue-router'
import { routes } from '@/router/routes'
import { useAppCtl } from '@/store/app'
import { loadAppConf } from '@/config'

const router: Router = createRouter({
  history: createWebHistory(import.meta.env.VITE_APP_PREFIX),
  routes,
})

export function updateRouterByServes(serves: any[]) {
  serves &&
    serves.forEach((item) => {
      router.addRoute('main', {
        path: `${item.prefix}/:chapters*`,
        name: item.name,
        component: () => import('@/views/appList/AppList.vue'),
        meta: {
          title: item.name,
          roles: [],
          serve: item,
        },
      })
    })
}

router.beforeEach(async (to, from, next) => {
  next()
})

router.afterEach(() => {
  // do nothing
})

export default router
