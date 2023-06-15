<template>
  <div :id="name" class="app-view" />
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { loadMicroApp } from 'qiankun'
import type { Serve } from '@/beans'

defineOptions({ name: 'AppList' })

const route = useRoute()
const { name, domain, prefix, devDomain } = route.meta.serve as Serve
const servOpts: any = {
  name,
  entry: import.meta.env.DEV ? devDomain : domain,
  container: `#${name}`,
  activeRule: prefix,
  props: { name },
}

let microApp: any = null
onMounted(() => {
  if (microApp) {
    return
  }
  microApp = loadMicroApp(servOpts)
  microApp.mountPromise.then(() => {
    // 微应用加载完成后回调
  })
})

onUnmounted(() => {
  if (!microApp) {
    return
  }
  microApp.unmount()
})
</script>

<style lang="scss">
.app-view {
  @apply w-full h-full;
  & > div {
    @apply w-full h-full;
  }
}
</style>
