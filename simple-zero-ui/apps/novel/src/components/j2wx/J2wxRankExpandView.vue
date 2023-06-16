<template>
  <div class="rank-expand">
    <div v-for="(item, index) in lineList" :key="index" class="line">
      <div class="line-label">{{ item.label }}:</div>
      <div class="line-val">{{ item.val }}</div>
    </div>
    <div class="chart-wrapper overflow-auto no-scrollbar mt-4">
      <j2wx-rank-chart :rank-data="rankData" is-increment />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, toRefs } from 'vue'
import type { J2RankBook } from '@/common'
import { formatFavoriteCount, formatRank } from '@/common'

defineOptions({ name: 'J2wxRankExpandView' })
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
})

const { data } = toRefs(props)
const rankData = computed(() => [data.value])

const lineList = [
  { label: '小说名称', val: data.value.book.name },
  { label: '作者', val: data.value.book.authorName },
  { label: '字数', val: data.value.book.size },
  { label: '标签', val: data.value.book.tags },
  { label: '类型', val: data.value.book.type },
  { label: '排行(涨幅)', val: formatRank(data.value as J2RankBook) },
  {
    label: '收藏(涨幅)',
    val: formatFavoriteCount(data.value as J2RankBook),
  },
]
</script>

<style scoped lang="scss">
.rank-expand {
  @apply pl-8;
  .line {
    @apply flex flex-row;
    & > div {
      @apply inline-block;
    }
    .line-label {
      @apply pr-2;
    }
    .line-val {
      @apply flex-grow font-bold;
    }
  }
}
</style>
