<template>
  <el-menu
    mode="horizontal"
    :ellipsis="false"
    :default-active="activeRoute"
    class="horizontal-menu"
  >
    <el-menu-item
      v-for="item in appConf.config.headers"
      :key="item.id"
      :index="item.path"
      @click="openMenuItem(item)"
    >
      {{ item.name }}
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import { useAppCtl } from '@/store/app'

defineOptions({
  name: 'CommonHMenu',
})

const appConf = useAppCtl()
const router = useRouter()
const activeRoute = computed(() => {
  let startRoutePath = '/'
  for (const headerItem of appConf.config.headers) {
    if (headerItem.path === router.currentRoute.value.path) {
      return headerItem.path
    }
    if (router.currentRoute.value.path.startsWith(headerItem.path)) {
      if (headerItem.path.length > startRoutePath.length) {
        startRoutePath = headerItem.path
      }
    }
  }
  return startRoutePath
})

const openMenuItem = (item: { path: string }) => {
  router.push(item.path)
}
</script>

<style lang="scss" scoped>
.horizontal-menu {
  @apply border-b-0;
}
</style>
