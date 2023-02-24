<template>
  <div ref="chartRoot" class="chart-root" />
</template>

<script setup lang="ts">
import { computed, onMounted, toRefs } from 'vue'

import { strIntercept } from '@leiax00/utils'
import type { J2RankBook } from '@/common'
import { echarts, toChartData } from '@/common'

defineOptions({ name: 'J2wxRankChart' })
const props = defineProps({
  rankData: {
    type: Array,
    required: true,
  },
})
const { rankData } = toRefs(props)
const chartData = computed(() => {
  return toChartData(rankData.value)
})
const books = computed(() => {
  return rankData.value.map((item) => (item as J2RankBook).book)
})

const chartRoot = ref(null)
onMounted(() => {
  const myChart = echarts.init(chartRoot.value)
  const option = constructOption(chartData.value)
  myChart.setOption(option)
})

function constructOption(_rawData: any) {
  const datasetWithFilters: echarts.DatasetComponentOption[] = []
  const seriesList: echarts.SeriesOption[] = []
  echarts.util.each(books.value, (book) => {
    const datasetId = `dataset_${book.id}`
    datasetWithFilters.push({
      id: datasetId,
      fromDatasetId: 'dataset_raw',
      transform: {
        type: 'filter',
        config: {
          and: [{ dimension: 'id', '=': book.id }],
        },
      },
    })
    seriesList.push({
      type: 'line',
      datasetId,
      showSymbol: false,
      name: book.name,
      endLabel: {
        show: true,
        formatter(params: any) {
          return `${strIntercept(book.name, 10)}: ${params.value[4]}`
        },
      },
      labelLayout: {
        moveOverlap: 'shiftY',
      },
      emphasis: {
        focus: 'series',
      },
      encode: {
        x: 'time',
        y: 'favoriteCount',
        label: ['name', 'favoriteCount'],
        itemName: 'time',
        tooltip: ['favoriteCount'],
      },
    })
  })

  return {
    animationDuration: 3000,
    dataset: [
      {
        id: 'dataset_raw',
        source: _rawData,
      },
      ...datasetWithFilters,
    ],
    title: {
      text: '今日收藏变化趋势',
    },
    tooltip: {
      order: 'valueDesc',
      trigger: 'axis',
    },
    xAxis: {
      type: 'time',
      nameLocation: 'middle',
    },
    yAxis: {
      name: '收藏数',
    },
    grid: {
      right: 160,
    },
    series: seriesList,
  }
}
</script>

<style scoped>
.chart-root {
  width: 600px;
  height: 300px;
}
</style>