import serve from '@/common/apis/serve'

function searchBookByName(bookName: string) {
  return serve.get(`/search/${bookName}`)
}

function getChapter(bid: string, cid: string) {
  return serve.get(`/chapter/${bid}/${cid}`)
}

export default {
  searchBookByName,
  getChapter,
}
