<template>
  <div class="common-header">
    <div class="header-logo">
      <div class="menu" @click="changeAsideStatus">
        <sz-icon :icon-class="showAsideIcon" class="icon-24" />
      </div>
      <div class="logo ml-3 sm:ml-0">
        <router-link class="nav-item" to="/">
          <img :src="logoUrl" alt="Simple Zero" class="h-8" />
        </router-link>
      </div>
    </div>
    <div class="flex-grow header-menu hidden sm:flex">Header Menu</div>
    <div class="header-right">
      <div class="block sm:hidden">SM Right Nav</div>
      <div class="hidden sm:block">MD Right Nav</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useApp } from '@/store/app'

defineOptions({
  name: 'CommonHeader',
})
const appConf = useApp()
const logoUrl = appConf.logoUrl
const showAsideIcon = computed(() => {
  return appConf.uiCtl.showAside ? 'shouqicaidan' : 'zhankaicaidan'
})
const changeAsideStatus = () => {
  appConf.uiCtl.showAside = !appConf.uiCtl.showAside
}
</script>

<style lang="scss" scoped>
.common-header {
  @apply flex flex-row justify-between items-center py-4;
  .nav-item {
    @apply py-4 leading-8 h-8;
  }
  .header-logo {
    div {
      @apply inline-block align-middle;
    }
    .menu {
      @apply sm:hidden;
    }
    .logo {
      @apply mr-6;
    }
  }
}
</style>
