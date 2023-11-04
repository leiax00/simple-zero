import { useStorage } from '@vueuse/core'
import type { RemovableRef } from '@vueuse/core'
import type { BookBase } from '@/views/bean'

export type ReadPos = {
  curPos: number // 当前的scrollTop
  pageWidth?: number // 当前的页面宽度
  pageHeight?: number // 当前的页面宽度
}

export type ReadProgress = {
  cid: string
  pos: ReadPos
}

export type Novel = {
  book: BookBase
  readProgress?: ReadProgress
}

export type NovelManager = {
  novels: Record<string, Novel>
}

export const novelManager: RemovableRef<NovelManager> = useStorage('novel-list', {
  novels: {},
})

export const add2BookList = function (novel: Novel) {
  novelManager.value.novels[novel.book.bid] = novel
}

export const removeFromBookList = function (novel: Novel) {
  delete novelManager.value.novels[novel.book.bid]
}

export const removeFromBookListById = function (id: string) {
  removeFromBookList({ id })
}

export const calcCurPos = function (bid: string): number {
  const novel = novelManager.value.novels[bid]
  const curWidth = document.documentElement.scrollWidth
  const curHeight = document.documentElement.scrollHeight
  if (!novel || !novel.readProgress || novel.readProgress.pos === 0) {
    return 0
  }
  const { curPos, pageWidth, pageHeight } = novel.readProgress.pos
  if (curWidth === pageWidth) {
    return curPos
  }
  // 计算不一定精准, 给20px冗余
  return Math.max(Math.floor((curPos * curHeight) / pageHeight) - 20, 0)
}

export const updateReadProgress = function (bid: string, cid: string, curPos: number) {
  const novel = novelManager.value.novels[bid]
  if (!novel) {
    return
  }
  novel.readProgress = {
    cid,
    pos: {
      curPos,
      pageWidth: document.documentElement.scrollWidth,
      pageHeight: document.documentElement.scrollHeight,
    },
  }
}

export const formatImgUrl = (url: string) => {
  console.log(`${url} -- ${location.protocol}`)
  if (!url.startsWith(location.protocol)) {
    url = `${location.origin}/api${new URL(url).pathname}`
  }
  return url
}
