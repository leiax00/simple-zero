<template>
  <el-table v-loading="tableData.length === 0" :data="tableData">
    <el-table-column
      v-for="(item, index) in tableColumns"
      :key="index"
      :type="item.type"
      :prop="item.key"
      :label="item.label"
      :width="item.width"
    >
      <template #default="{ row }">
        <div v-if="isText(item)" class="table-text">
          {{ item.formatter ? item.formatter(row) : row[item.key] }}
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'

defineOptions({ name: 'J2wxRankTable' })
const props = defineProps({
  tableData: {
    type: Array,
    required: true,
  },
})
const { tableData } = toRefs(props)

const formatScore = (row: any) => {
  const statLen = row.statList.length
  const score = row.statList[statLen - 1].score
  const prevScore = row.statList[0].score
  return `${score}(${score - prevScore})`
}
const formatName = (row: any) => {
  return row.book.name
}
const formatAuthor = (row: any) => {
  return row.book.authorName
}
const formatFavoriteCount = (row: any) => {
  const statLen = row.statList.length
  const score = row.statList[statLen - 1].favoriteCount
  const prevScore = row.statList[0].favoriteCount
  return `${score}(${score - prevScore})`
}

const tableColumns: {
  key: string
  label?: string
  type?: string
  width?: string | number
  formatter?: any
}[] = [
  { key: 'id', type: 'expand', width: 40 },
  // { key: 'score', label: '排名', width: 80, formatter: formatScore },
  { key: 'name', label: '小说', formatter: formatName },
  // { key: 'author', label: '作者', formatter: formatAuthor },
  { key: 'favorite', label: '收藏(今)', formatter: formatFavoriteCount },
]

const isText = (item: { type?: string }) => {
  return item.type === undefined || item.type === 'text'
}
</script>

<style scoped></style>
