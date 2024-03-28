<template>
  <div class="layout-main w-full h-full">
    <component :is="layout" />
    <el-backtop :bottom="64" :right="24">
      <div>UP</div>
    </el-backtop>
  </div>
</template>

<script setup lang="ts">
import layoutTheme from './layoutTheme'
import { useApp } from '@/store/app'

defineOptions({ name: 'Layout' })
const { config } = useApp()

const layoutName = config.common?.theme || 'MinimalistLayout'
const layout = shallowRef(layoutTheme[layoutName])
</script>

<style scoped></style>
