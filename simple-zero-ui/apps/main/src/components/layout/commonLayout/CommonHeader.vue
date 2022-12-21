<template>
  <div class="common-header">
    <div class="header-logo">
      <a class="nav-item" href="/">
        <img :src="logoUrl" alt="Simple Zero" class="h-8" />
      </a>
    </div>
    <div class="flex-grow header-menu hidden sm:flex">Header Menu</div>
    <div class="header-right">
      <div class="block sm:hidden">SM Right Nav</div>
      <div class="hidden sm:block">MD Right Nav</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useApp } from '@/store/app'

defineOptions({
  name: 'CommonHeader',
})
const appConf = useApp()
const logoUrl = appConf.logoUrl
</script>

<style lang="scss" scoped>
.common-header {
  @apply flex flex-row justify-between items-center py-4;
  .nav-item {
    @apply py-4 leading-8 h-8;
  }
  .header-logo {
    @apply max-w-logo flex-logo;
  }
}
</style>
