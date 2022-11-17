<template>
  <div :id="route.meta.serve.name" />
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { loadMicroApp } from 'qiankun'

defineOptions({ name: 'AppList' })

const route = useRoute()

const servOpts = {
  name: route.meta.serve.name,
  entry: route.meta.serve.domain,
  container: `#${route.meta.serve.name}`,
  activeRule: route.meta.serve.prefix,
  props: { name: route.meta.serve.name },
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

<style scoped></style>
