import { useStorage } from '@vueuse/core'
import type { RemovableRef } from '@vueuse/core'
import type { Engin, EnginManager } from '@/beans/engin'

export const defaultEnginList: Engin[] = [
  {
    key: 'baidu',
    label: '百度',
    awake: 'bd',
    uri: 'https://www.baidu.com/s?wd=',
    placeholder: '百度一下',
  },
  {
    key: 'google',
    label: '谷歌',
    awake: 'gg',
    uri: 'https://www.google.com/search?q=',
    placeholder: 'Google 搜索',
  },
  {
    key: 'github',
    label: 'github',
    awake: 'gh',
    uri: 'https://github.com/search?q=',
    placeholder: 'github 搜索',
  },
  {
    key: 'douban',
    label: '豆瓣',
    awake: 'db',
    uri: 'https://www.douban.com/search?q=',
    placeholder: '豆瓣搜索',
  },
  {
    key: 'iconfont',
    label: 'Iconfont',
    awake: 'if',
    uri: 'https://www.iconfont.cn/search/index?searchType=icon&q=',
    placeholder: 'Iconfont SVG 图标搜索',
  },
]
export const searchEngin: RemovableRef<EnginManager> = useStorage('searchEngin', {
  active: 'baidu',
  enginList: defaultEnginList,
})

export const toSearch = function (baseUri: string, searchKey: string) {
  window.open(baseUri + searchKey)
}
