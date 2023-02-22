import serve from '@/common/apis/serve'

export function searchBookByName(bookName: string) {
  return serve.get(`/search/${bookName}`)
}

export function getChapter(bid: string, cid: string) {
  return serve.get(`/chapter/${bid}/${cid}`)
}

export function getJ2wxRankList(channelKey: string) {
  return serve.get(`/j2wx/${channelKey}/rankList`)
}
