import type { RouteRecordRaw } from 'vue-router'

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home',
    children: [
      {
        path: '/home',
        component: () => import('@/views/home/Home.vue'),
        meta: { title: 'Home', roles: [] },
      },
    ],
  },
]

export const asyncRoutes = []
