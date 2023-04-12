<script setup lang="ts">
import { computed } from 'vue'
import { qiankunWindow } from 'vite-plugin-qiankun/es/helper'

const appClazz = computed(() => {
  const classList = ['app-main']
  if (!qiankunWindow.__POWERED_BY_QIANKUN__) {
    classList.push('root-with-no-micro')
  }
  return classList
})
</script>

<template>
  <router-view :key="$route.fullPath" :class="appClazz" />
</template>

<style scoped></style>
