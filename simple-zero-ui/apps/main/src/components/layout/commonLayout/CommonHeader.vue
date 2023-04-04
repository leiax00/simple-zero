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
    <div class="header-right">
      <sz-theme-toggler />
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
  .header-menu {
    @apply flex-grow hidden sm:flex;
  }
  .header-right {
    .header-lt-sm {
      @apply block sm:hidden;
    }
    .header-gt-sm {
      @apply hidden sm:block;
    }
  }
}
</style>
