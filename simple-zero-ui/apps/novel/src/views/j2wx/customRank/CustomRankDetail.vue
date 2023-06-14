<script setup lang="ts">
import type { CustomRank, J2RankBook } from '@/common'
import { rankList } from '@/views/j2wx/customRank/bean'
import common from '@/common'

defineOptions({ name: 'CustomRankDetail' })
const props = defineProps<{
  id: number
}>()
const { id } = toRefs(props)
const pageData = reactive<{
  selectRank: CustomRank
  selectRankInfo: J2RankBook[]
}>({
  selectRank: rankList.value[id.value],
  selectRankInfo: [],
})

onMounted(() => {
  // todo 加载数据
  console.log(JSON.stringify(pageData.selectRank))
  common.apis.getJ2wxCustomRankInfo(pageData.selectRank.id).then((resp) => {
    pageData.selectRankInfo = resp.data
  })
})
</script>

<template>
  <div>
    <j2wx-rank-table :table-data="pageData.selectRankInfo" />
  </div>
</template>

<style scoped lang="scss"></style>
