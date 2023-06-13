<template>
  <el-table
    ref="rankTable"
    v-loading="tableData.length === 0"
    :data="tableData"
    :row-key="getRowKey"
    :expand-row-keys="pageData.expandList"
    @row-click="onRowClick"
  >
    <el-table-column
      v-for="(item, index) in tableColumns"
      :key="index"
      :type="item.type as string"
      :prop="item.key"
      :label="item.label as string"
      :width="item.width as number"
    >
      <template #default="{ row }">
        <div v-if="isText(item)" class="table-text">
          {{ item.formatter ? item.formatter(row) : row[item.key] }}
        </div>
        <j2wx-rank-expand-view v-else-if="isExpand" :data="row" />
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
import { computed, reactive, toRefs } from 'vue'
import type { J2RankBook, TableColumn } from '@/common'
import { breakpoints, formatFavoriteCount, formatRank } from '@/common'
import J2wxRankExpandView from '@/components/j2wx/J2wxRankExpandView.vue'

defineOptions({ name: 'J2wxRankTable' })
const props = defineProps({
  tableData: {
    type: Array,
    required: true,
  },
})
const { tableData } = toRefs(props)

const tableColumns = computed((): TableColumn[] => {
  const tmp: TableColumn[] = [{ key: 'id', type: 'expand', width: 40 }]
  if (breakpoints.greaterOrEqual('sm').value) {
    tmp.push({ key: 'score', label: '排名', width: 80, formatter: formatRank })
  }
  tmp.push({ key: 'name', label: '小说', formatter: formatName })
  if (breakpoints.greaterOrEqual('md').value) {
    tmp.push({ key: 'author', label: '作者', formatter: formatAuthor })
  }
  tmp.push({
    key: 'favorite',
    label: '收藏(今)',
    formatter: formatFavoriteCount,
  })
  return tmp
})

const pageData = reactive<{
  singleExpand?: boolean
  expandList: string[]
}>({
  singleExpand: true,
  expandList: [],
})

const formatName = (row: J2RankBook) => {
  return row.book.name
}
const formatAuthor = (row: J2RankBook) => {
  return row.book.authorName
}

const getRowKey = (row: any): string => `${row.book.id}`

/**
 * 控制行点击时是否展开, 支持单独展开一行
 * @param row
 */
const onRowClick = (row: any) => {
  const rowKey = getRowKey(row)
  if (pageData.singleExpand) {
    pageData.expandList = pageData.expandList[0] === rowKey ? [] : [rowKey]
    return
  }
  if (pageData.expandList.includes(rowKey)) {
    pageData.expandList = pageData.expandList.filter((item) => item !== rowKey)
  } else {
    pageData.expandList.push(rowKey)
  }
}

const isText = (item: { type?: string }) => {
  return item.type === undefined || item.type === 'text'
}
const isExpand = (item: { type?: string }) => {
  return item.type === 'expand'
}
</script>

<style scoped></style>
