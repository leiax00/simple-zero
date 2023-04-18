<template>
  <div class="color-calc-main">
    <div class="title-level-2">颜色计算器</div>
    <div class="content-wrapper">
      <div class="flex">
        <div class="w-1/4 leading-8">当前颜色</div>
        <el-input v-model="currentColor" class="flex-grow" />
      </div>
      <div class="flex">
        <div class="w-1/4 leading-8">颜色名称</div>
        <div class="flex-grow">{{ colorName }}</div>
      </div>
      <div class="flex">
        <div class="w-1/4 leading-8">HEX</div>
        <div class="flex-grow">{{ hex }}</div>
      </div>
      <div class="flex">
        <div class="w-1/4 leading-8">RGB</div>
        <div class="flex-grow">{{ rgb }}</div>
      </div>
      <div class="flex">
        <div class="w-1/4 leading-8">RGBA</div>
        <div class="flex-grow">{{ rgba }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import chroma from 'chroma-js'

defineOptions({ name: 'ColorCalcView' })

const currentColor = ref('#ffffff')
const colorName = computed(() => chroma(currentColor.value).name())
const rgb = computed(() => chroma(currentColor.value).rgb())
const rgba = computed(() => chroma(currentColor.value).rgba())
const hex = computed(() => chroma(currentColor.value).hex())
</script>

<style scoped></style>
