import type { RouteRecordRaw } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    name: 'main',
    children: [
      {
        path: '/home',
        component: () => import('@/views/Home.vue'),
        meta: { title: 'Home', roles: [] },
      },
    ],
  },
  {
    path: '/login',
    component: () => import('@/views/login/Login.vue'),
    meta: { title: 'Login', roles: [] },
  },
  {
    path: '/404',
    component: () => import('@/views/error/Page404.vue'),
    meta: { hidden: true },
  },
  { path: '/index', name: 'home', redirect: '/home' },
  { path: '/:pathMatch(.*)*', name: 'not-found', redirect: '/404' },
]

export const asyncRoutes = []
