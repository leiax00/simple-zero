import Layout from '@/components/layout/index.vue'
import { RouteRecordRaw } from 'vue-router'
// @ts-ignore
import settings from '@/settings.yaml'

function getAppRoutes() {
  const serveList = settings.services
  const routes = []
  serveList.forEach(item => {
    routes.push({
      path: item.prefix,
      name: item.name,
      component: () => import('@/views/appList/AppList.vue'),
      meta: {
        title: item.name,
        roles: [],
        serve: item
      }
    })
  })
  return routes
}

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: Layout,
    redirect: '/index',
    children: [
      {
        path: '/index',
        component: () => import('@/views/Home.vue'),
        meta: { title: 'Home', roles: [] }
      },
      ...getAppRoutes()
    ]
  },
  {
    path: '/404',
    component: () => import('@/views/error/Page404.vue'),
    meta: { hidden: true }
  },
  { path: '/:pathMatch(.*)*', name: 'not-found', redirect: '/404' }
]

export const asyncRoutes = []
