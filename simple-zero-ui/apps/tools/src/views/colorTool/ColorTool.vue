<template>
  <div class="color-main">
    <div class="title-level-1">颜色选择与计算</div>
    <div class="content-wrapper">
      <color-legend class="w-full" :pick-color="pickColor" />
      <color-calc-view class="w-full" :pick-color="pickColor" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import ColorLegend from './ColorLegend.vue'
import ColorCalcView from './ColorCalcView.vue'

defineOptions({ name: 'ColorTool' })
const pickColor = ref('#ffffff')
</script>

<style scoped lang="scss">
.color-main {
  @apply bg-body p-4 bg-white/5 rounded-xl;
  .content-wrapper {
    @apply flex flex-wrap gap-16;
    @apply lg:flex-nowrap lg:gap-8;
    @apply xl:gap-16;
  }
}
</style>
