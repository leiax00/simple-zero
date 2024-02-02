import * as echarts from 'echarts/core'
import {
  DatasetComponent,
  GridComponent,
  TitleComponent,
  TooltipComponent,
  TransformComponent,
} from 'echarts/components'
import { LineChart } from 'echarts/charts'
import { LabelLayout, UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import type { LineSeriesOption } from 'echarts/charts'
import type {
  DatasetComponentOption,
  GridComponentOption,
  TitleComponentOption,
  TooltipComponentOption,
} from 'echarts/components'

echarts.use([
  DatasetComponent,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  TransformComponent,
  LineChart,
  CanvasRenderer,
  LabelLayout,
  UniversalTransition,
])

export type EChartsOption = echarts.ComposeOption<
  DatasetComponentOption | TitleComponentOption | TooltipComponentOption | GridComponentOption | LineSeriesOption
>

export default echarts
