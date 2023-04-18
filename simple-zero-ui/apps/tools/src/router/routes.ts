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
      {
        path: '/color',
        component: () => import('@/views/colorTool/ColorTool.vue'),
        meta: { title: 'Color View', roles: [] },
      },
    ],
  },
]

export const asyncRoutes = []
