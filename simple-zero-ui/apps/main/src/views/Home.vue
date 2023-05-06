<template>
  <div class="main-home">
    <engin-search class="search" />
    <div class="route-list">
      <template v-for="menuGroup in config.menus">
        <sz-link
          v-for="item in menuGroup.data"
          :key="item.id"
          :type="item.type || 'route'"
          :to="item.path"
        >
          <el-card v-ripple shadow="always">{{ item.name }}</el-card>
        </sz-link>
      </template>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { EtcdConf } from '@/beans'
import { useApp } from '@/store/app'

defineOptions({ name: 'Home' })
const appStore = useApp()
const config = appStore.config as EtcdConf
</script>

<style scoped lang="scss">
.main-home {
  .search {
    @apply m-auto w-full lg:w-1/2;
  }
  .route-list {
    @apply common-grid-1 mt-4 sm:mt-8 md:mt-12 lg:mt-16;
    .sz-link {
      @apply w-full;
    }
  }
}
</style>
