<template>
  <div class="main-home">
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
  .route-list {
    @apply common-grid-1;
    .sz-link {
      @apply w-full;
    }
  }
}
</style>
