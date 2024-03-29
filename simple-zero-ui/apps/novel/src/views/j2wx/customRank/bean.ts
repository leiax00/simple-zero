import { useStorage } from '@vueuse/core'
import type { RemovableRef } from '@vueuse/core'
import type { CustomRank } from '@/common'

export const getDefaultRank = (): CustomRank => ({ name: '', password: '', bookIdList: [] })

const defaultRankList: Record<string, CustomRank> = {}
export const rankList: RemovableRef<Record<string, CustomRank>> = useStorage('custom-rank-list', defaultRankList)
export const selectRankCond: RemovableRef<{
  rank: CustomRank
  beforeHour: number
}> = useStorage('local-select-custom-rank', {
  rank: {} as CustomRank,
  beforeHour: 7 * 24,
})

export const TYPE_OPERATE = {
  SHOW: 'show',
  ADD: 'add',
  LOAD: 'load',
  DELETE: 'delete',
}
