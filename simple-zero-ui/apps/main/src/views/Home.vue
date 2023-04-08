<template>
  <div class="main-home">
    <engin-search class="search" />
    <div class="route-list">
      <sz-link
        v-for="item in appStore.config.menus"
        :key="item.id"
        type="route"
        :to="item.path"
      >
        <el-card v-ripple shadow="always">{{ item.name }}</el-card>
      </sz-link>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useApp } from '@/store/app'

defineOptions({ name: 'Home' })
const appStore = useApp()
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
