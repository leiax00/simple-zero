import type { RouteRecordRaw } from 'vue-router'
import Layout from '@/components/layout/index.vue'

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: Layout,
    redirect: '/index',
    name: 'main',
    children: [
      {
        path: '/index',
        component: () => import('@/views/Home.vue'),
        meta: { title: 'Home', roles: [] },
      },
    ],
  },
  {
    path: '/404',
    component: () => import('@/views/error/Page404.vue'),
    meta: { hidden: true },
  },
  { path: '/:pathMatch(.*)*', name: 'not-found', redirect: '/404' },
]

export const asyncRoutes = []
