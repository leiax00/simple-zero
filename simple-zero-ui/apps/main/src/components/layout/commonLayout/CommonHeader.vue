<template>
  <div class="common-header">
    <div class="header-logo">
      <div class="menu" @click="changeAsideStatus">
        <sz-icon :icon-class="showAsideIcon" class="icon-5" />
      </div>
      <div class="logo ml-3 sm:ml-0">
        <router-link class="nav-item" to="/">
          <img :src="logoUrl" alt="Simple Zero" class="h-8" />
        </router-link>
      </div>
    </div>
    <div class="header-right">
      <sz-theme-toggler />
      <sz-icon v-if="config.common.github" icon-class="github" class="cursor-pointer icon-6" @click="toMyGithub" />
      <sz-icon icon-class="user" class="cursor-pointer icon-6" @click="toLoginPage" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useApp } from '@/store/app'

defineOptions({
  name: 'CommonHeader',
})
const { logoUrl, uiCtl, config } = useApp()
const showAsideIcon = computed(() => {
  return uiCtl.showAside ? 'shouqicaidan' : 'zhankaicaidan'
})
const router = useRouter()

const changeAsideStatus = () => {
  uiCtl.showAside = !uiCtl.showAside
}

const toMyGithub = () => {
  window.open(config.common.github)
}
const toLoginPage = () => {
  router.push({ path: '/login' })
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
      @apply sm:hidden align-top;
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
    & > div {
      @apply align-middle;
      & + div {
        @apply ml-4;
      }
    }
  }
}

.icon-5 {
  @apply w-5 h-5;
}
</style>
