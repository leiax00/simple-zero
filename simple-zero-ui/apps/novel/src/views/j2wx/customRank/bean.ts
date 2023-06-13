import { useStorage } from '@vueuse/core'
import type { RemovableRef } from '@vueuse/core'

export type CustomRank = {
  id: number
  name: string
  password: string
  desc?: string
  bookIdList: string[]
}

export const getDefaultRank = (): CustomRank => ({ id: -1, name: '', password: '', bookIdList: [] })

const defaultRankList: Record<string, CustomRank> = {}
export const rankList: RemovableRef<Record<string, CustomRank>> = useStorage('custom-rank-list', defaultRankList)

export const TYPE_OPERATE = {
  SHOW: 'show',
  ADD: 'add',
  LOAD: 'load',
  DELETE: 'delete',
}
