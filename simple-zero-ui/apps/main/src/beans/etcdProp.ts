import type { Engin } from '@/beans/engin'

export type Menu = {
  id: string
  name: string
  icon?: string
  showWeight?: number
  data: MenuItem[]
}

export type MenuItem = {
  id: string
  name: string
  path: string
  icon?: string
  showWeight?: number
  // {@link LINK_TYPE}
  type?: 'route' | 'link' | 'route_2_link' | 'link_2_route'
}

export type Serve = {
  id?: string
  name: string
  prefix: string
  domain: string
  devDomain?: string
}

export type etcdCommon = {
  copyRight: string
  firstRun: string
  static: string
  svgUri: string
  searchEngin?: Engin[]
}

export type EtcdConf = {
  common?: etcdCommon
  menus: Menu[]
  serves: Serve[]
}
