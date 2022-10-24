import serve from '@/common/apis/serve'

function searchBookByName(bookName: String) {
  return serve.get(`/search/${bookName}`)
}

export default {
  searchBookByName
}
