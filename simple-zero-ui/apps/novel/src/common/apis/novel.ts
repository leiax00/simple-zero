import type { AxiosResponse } from 'axios'
import type { CustomRank } from '@/common'
import serve from '@/common/apis/serve'

export type CommonResp = {
  code: number
  data: any
  msg: string
}

export function searchBookByName(bookName: string): Promise<CommonResp> {
  return serve.get(`/search/${bookName}`)
}

export function getChapter(bid: string, cid: string): Promise<CommonResp> {
  return serve.get(`/chapter/${bid}/${cid}`)
}

export function getJ2wxRankList(channelKey: string): Promise<CommonResp> {
  return serve.get(`/j2wx/channel/${channelKey}`)
}

export function getJ2wxRankInfo(channelKey: string, rankId: string): Promise<CommonResp> {
  return serve.get(`/j2wx/channel/${channelKey}/${rankId}`)
}

export function getJ2wxCustomRankInfo(rankId: any): Promise<CommonResp> {
  return serve.get(`/j2wx/custom-rank/${rankId}`)
}

export function createCustomRank(rank: CustomRank): Promise<CommonResp> {
  return serve.post(`/j2wx/custom-rank/new`, rank)
}

export function loadCustomRankByKey(key: string): Promise<CommonResp> {
  return serve.get(`/j2wx/custom-rank/load?key=${key}`)
}

export function deleteCustomRank(rankId: number): Promise<CommonResp> {
  return serve.delete(`/j2wx/custom-rank/del?ids=${rankId}`)
}

export function addNovel2CustomRank(rankId: number, novelIds: Array<string> | string): Promise<CommonResp> {
  return serve.put(`/j2wx/custom-rank/add-novel`, { rankId, ids: novelIds })
}

export function delNovelFromCustomRank(rankId: number, novelIds: Array<string> | string): Promise<CommonResp> {
  return serve.delete(
    `/j2wx/custom-rank/del-novel?rankId=${rankId}&ids=${typeof novelIds === 'string' ? novelIds : novelIds.join(',')}`
  )
}
