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
          <el-menu-item
            v-for="item in appConf.config.headers"
            :key="item.id"
            :index="item.path"
            @click="openMenuItem(item)"
          >
            {{ item.name }}
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </div>
    <div class="aside-footer" @click="appConf.uiCtl.showAside = false">
      ⬅ 收起
    </div>
  </div>
</template>
<script setup lang="ts">
import { useApp } from '@/store/app'

defineOptions({
  name: 'CommonAside',
})
const appConf = useApp()
const logoUrl = appConf.logoUrl

const router = useRouter()
let activeRoute = router.currentRoute.value.path
const openMenuItem = (item: { path: string }) => {
  router.push(item.path)
  activeRoute = item.path
  appConf.uiCtl.showAside = false
}
</script>

<style lang="scss" scoped>
.main-aside {
  @apply flex flex-col h-full;
  .aside-footer {
    @apply text-center h-12 py-2 leading-8 shadow-aside-red-top;
  }
}
</style>
