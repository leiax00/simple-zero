export type Menu = {
  id: string
  name: string
  icon?: string
  data: MenuItem[]
}

export type MenuItem = {
  id: string
  name: string
  path: string
  icon?: string
  // {@link LINK_TYPE}
  type?: 'route' | 'link' | 'route_2_link' | 'link_2_route'
}

export type Serve = {
  id?: string
  name: string
  prefix: string
  domain: string
}

export type etcdCommon = {
  copyRight: string
  firstRun: string
  static: string
  svgUri: string
}

export type EtcdConf = {
  common?: etcdCommon
  menus: Menu[]
  serves: Serve[]
}
