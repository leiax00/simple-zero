<template>
  <div ref="chartRoot" class="chart-root" />
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, toRefs } from 'vue'

import { strIntercept } from '@leiax00/utils'
import colors from 'tailwindcss/colors'
import { useDark, useThrottleFn, useWindowSize } from '@vueuse/core'
import type { J2RankBook } from '@/common'
import { echarts, toChartData } from '@/common'

defineOptions({ name: 'J2wxRankChart' })
const props = defineProps({
  rankData: {
    type: Array,
    required: true,
  },
  isIncrement: {
    type: Boolean,
    default: false,
  },
})

const isDark = useDark({
  storageKey: 'theme-appearance',
})

const { width, height } = useWindowSize()

const { rankData, isIncrement } = toRefs(props)
const chartData = computed(() => {
  return toChartData(rankData.value, isIncrement.value)
})
const books = computed(() => {
  return rankData.value.map((item) => (item as J2RankBook).book)
})

const chartRoot = ref(null)

const pageData = reactive({
  myChart: null,
  option: {},
})

onMounted(() => {
  pageData.myChart = echarts.init(chartRoot.value)
  pageData.option = constructOption(chartData.value)
  pageData.myChart.setOption(pageData.option)
})

watch(isDark, () => {
  if (isDark.value) {
    pageData.option.yAxis.splitLine.lineStyle.color = colors.zinc['700']
  } else {
    pageData.option.yAxis.splitLine.lineStyle.color = colors.zinc['300']
  }
  pageData.option.series?.forEach((item) => {
    item.lineStyle.color = isDark.value
      ? colors.emerald['500']
      : colors.emerald['500']
    item.endLabel.color = isDark.value
      ? colors.emerald['500']
      : colors.emerald['500']
  })
  pageData.myChart.setOption(pageData.option)
})

watch(
  width,
  useThrottleFn(
    () => {
      pageData.myChart.dispose()
      const newChart = echarts.init(chartRoot.value)
      newChart.setOption(pageData.option)
      newChart.resize()
      pageData.myChart = newChart
    },
    500,
    true,
    false
  )
)

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
      coordinateSystem: 'cartesian2d',
      endLabel: {
        show: true,
        formatter(params: any) {
          return `${strIntercept(book.name, 10)}: ${params.value[4]}`
        },
        color: isDark.value ? colors.emerald['400'] : colors.emerald['500'],
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
      lineStyle: {
        color: isDark.value ? colors.emerald['500'] : colors.emerald['500'],
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
      text: isIncrement.value ? '今日收藏增量变化' : '今日收藏变化',
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
      type: 'value',
      name: '增量收藏数',
      splitLine: {
        // 设置 y 轴对齐的线的颜色
        lineStyle: {
          color: isDark.value ? colors.zinc['700'] : colors.zinc['300'],
        },
      },
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
  @apply w-full;
  min-width: 600px;
  height: 300px;
}
</style>
