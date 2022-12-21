<template>
  <div :id="route.meta.serve.name" />
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { loadMicroApp } from 'qiankun'

defineOptions({ name: 'AppList' })

const route = useRoute()
const { name, domain, prefix } = route.meta.serve as {
  name: string
  domain: string
  prefix: string
}
const servOpts = {
  name,
  entry: domain,
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

<style scoped></style>
