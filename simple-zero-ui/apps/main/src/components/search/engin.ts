import { useStorage } from '@vueuse/core'
import type { RemovableRef } from '@vueuse/core'

export type Engin = {
  key: string
  label: string
  uri: string
  placeholder: string
}

export type EnginManager = {
  active: string
  enginList: Engin[]
}

export const enginList: Engin[] = [
  {
    key: 'baidu',
    label: '百度',
    uri: 'https://www.baidu.com/s?wd=',
    placeholder: '百度一下',
  },
  {
    key: 'google',
    label: '谷歌',
    uri: 'https://www.google.com/search?q=',
    placeholder: 'Google 搜索',
  },
  {
    key: 'douban',
    label: '豆瓣',
    uri: 'https://www.douban.com/search?q=',
    placeholder: '豆瓣搜索',
  },
  {
    key: 'iconfont',
    label: 'Iconfont',
    uri: 'https://www.iconfont.cn/search/index?searchType=icon&q=',
    placeholder: 'Iconfont SVG 图标搜索',
  },
]
export const searchEngin: RemovableRef<EnginManager> = useStorage(
  'searchEngin',
  {
    active: 'baidu',
    enginList,
  }
)

export const toSearch = function (baseUri: string, searchKey: string) {
  window.open(baseUri + searchKey)
}
