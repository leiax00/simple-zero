import type { CustomRank } from '@/common'
import serve from '@/common/apis/serve'

export function searchBookByName(bookName: string) {
  return serve.get(`/search/${bookName}`)
}

export function getChapter(bid: string, cid: string) {
  return serve.get(`/chapter/${bid}/${cid}`)
}

export function getJ2wxRankList(channelKey: string) {
  return serve.get(`/j2wx/channel/${channelKey}`)
}

export function getJ2wxRankInfo(channelKey: string, rankId: string) {
  return serve.get(`/j2wx/channel/${channelKey}/${rankId}`)
}

export function getJ2wxCustomRankInfo(rankId: number) {
  return serve.get(`/j2wx/custom-rank/${rankId}`)
}

export function createCustomRank(rank: CustomRank) {
  return serve.post(`/j2wx/custom-rank/new`, rank)
}

export function loadCustomRankByKey(key: string) {
  return serve.get(`/j2wx/custom-rank/load?key=${key}`)
}

export function deleteCustomRank(rankId: number) {
  return serve.delete(`/j2wx/custom-rank/del?ids=${rankId}`)
}

export function addNovel2CustomRank(rankId: number, novelIds: Array<string> | string) {
  return serve.put(`/j2wx/custom-rank/add-novel`, { rankId, ids: novelIds })
}

export function delNovelFromCustomRank(rankId: number, novelIds: Array<string> | string) {
  return serve.delete(
    `/j2wx/custom-rank/del-novel?rankId=${rankId}&ids=${typeof novelIds === 'string' ? novelIds : novelIds.join(',')}`
  )
}
