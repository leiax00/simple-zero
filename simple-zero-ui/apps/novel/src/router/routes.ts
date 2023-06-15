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
        path: '/chapter/:bid/:cid',
        name: 'chapter',
        component: () => import('@/components/book/Chapter.vue'),
        // props: route => ({ bid: route.params.bid, cid: route.params.cid }),
        props: true,
        meta: { title: '小说章节', roles: [] },
      },
    ],
  },
  {
    path: '/j2wx',
    redirect: '/j2wx/index',
    children: [
      {
        path: 'index',
        component: () => import('@/views/j2wx/J2wxHome.vue'),
        meta: { title: 'J2wx - 首页', roles: [] },
      },
      {
        path: 'channel/:channelKey',
        component: () => import('@/views/j2wx/J2wxChannel.vue'),
        props: true,
        meta: { title: 'J2wx - 分频', roles: [] },
      },
      {
        path: 'rank',
        component: () => import('@/views/j2wx/customRank/CustomRankDetail.vue'),
        meta: { title: 'J2wx - Personal Rank', roles: [] },
      },
      {
        path: 'rank/:id',
        component: () => import('@/views/j2wx/customRank/CustomRankDetail.vue'),
        props: true,
        meta: { title: 'J2wx - Personal Rank', roles: [] },
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
