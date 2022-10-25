import { RouteRecordRaw } from 'vue-router'

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home',
    children: [
      {
        path: '/home',
        component: () => import('@/views/home/Home.vue'),
        meta: { title: 'Home', roles: [] }
      },
      {
        path: '/chapter/:bid/:cid',
        name: 'chapter',
        component: () => import('@/views/chapter/Chapter.vue'),
        // props: route => ({ bid: route.params.bid, cid: route.params.cid }),
        props: true,
        meta: { title: '小说章节', roles: [] }
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
