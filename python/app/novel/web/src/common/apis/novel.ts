import serve from '@/common/apis/serve'

function searchBookByName(bookName: String) {
  return serve.get(`/search/${bookName}`)
}

function getChapter(bid: String, cid: String) {
  return serve.get(`/chapter/${bid}/${cid}`)
}

export default {
  searchBookByName,
  getChapter
}
