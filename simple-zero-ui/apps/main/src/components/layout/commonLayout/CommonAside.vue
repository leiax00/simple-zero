<template>
  <div class="main-aside">
    <div class="aside-logo pt-4 px-4">
      <router-link class="nav-item" to="/">
        <img :src="logoUrl" alt="Simple Zero" class="h-8" />
      </router-link>
    </div>

    <div class="aside-main flex-grow pt-6">
      <el-scrollbar>
        <el-menu :default-active="activeRoute">
          <template v-for="menuGroup in config.menus">
            <el-menu-item
              v-for="item in menuGroup.data"
              :key="item.id"
              :index="item.path"
              @click="openMenuItem(item)"
            >
              {{ item.name }}
            </el-menu-item>
          </template>
        </el-menu>
      </el-scrollbar>
    </div>
    <div class="aside-footer" @click="uiCtl.showAside = false">⬅ 收起</div>
  </div>
</template>
<script setup lang="ts">
import type { EtcdConf } from '@/beans'
import { useApp } from '@/store/app'

defineOptions({
  name: 'CommonAside',
})
const appConf = useApp()
const logoUrl = appConf.logoUrl
const uiCtl = appConf.uiCtl
const config = appConf.config as EtcdConf

const router = useRouter()
const activeRoute = computed(() => {
  let startRoutePath = '/'
  for (const menuGroup of config.menus) {
    for (const menu of menuGroup.data) {
      if (menu.path === router.currentRoute.value.path) {
        return menu.path
      }
      if (router.currentRoute.value.path.startsWith(menu.path)) {
        if (menu.path.length > startRoutePath.length) {
          startRoutePath = menu.path
        }
      }
    }
  }
  return startRoutePath
})
const openMenuItem = (item: { path: string }) => {
  router.push(item.path)
  appConf.uiCtl.showAside = false
}
</script>

<style lang="scss" scoped>
.main-aside {
  @apply flex flex-col h-full;
  .el-menu {
    @apply border-r-0;
  }
  .aside-footer {
    @apply text-center h-12 py-2 leading-8 shadow-aside-red-top;
  }
}
</style>
