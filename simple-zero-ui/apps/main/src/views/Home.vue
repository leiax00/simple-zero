<template>
  <div class="main-home">
    <engin-search class="search" />
    <template v-for="menuGroup in menus" :key="menuGroup.id">
      <div class="title-level-2 w-full lg:w-3/4 mx-auto mt-11">
        {{ menuGroup.name }}
      </div>
      <div class="route-list">
        <sz-link v-for="item in menuGroup.data" :key="item.id" :type="item.type || 'route'" :to="item.path">
          <el-card v-ripple shadow="always">{{ item.name }}</el-card>
        </sz-link>
      </div>
    </template>
  </div>
</template>

<script lang="ts" setup>
import type { Menu } from '@/beans'
import { useApp } from '@/store/app'

defineOptions({ name: 'Home' })
const appStore = useApp()
const menus = appStore.sortedMenus as Menu[]
</script>

<style scoped lang="scss">
.main-home {
  .search {
    @apply m-auto w-full lg:w-1/2;
  }
  .route-list {
    @apply common-grid-1;
    .sz-link {
      @apply w-full;
    }
  }
}
</style>
