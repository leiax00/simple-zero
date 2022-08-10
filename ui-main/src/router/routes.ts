import Layout from '@/components/layout/index.vue'
import { RouteRecordRaw } from 'vue-router'

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
      }
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
