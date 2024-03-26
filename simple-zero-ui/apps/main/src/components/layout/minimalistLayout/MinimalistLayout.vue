<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useDark, useToggle } from '@vueuse/core'
import MinimalistAside from './Aside.vue'
import MinimalistHeader from './Header.vue'
import MinimalistFooter from './footer.vue'

defineOptions({ name: 'MinimalistLayout' })
const layoutStyle = reactive({})
const route = useRoute()

useDark({
  storageKey: 'theme-appearance',
})
</script>

<template>
  <el-container class="minimalist-layout h-full" :style="layoutStyle">
    <el-aside class="aside">
      <minimalist-aside />
    </el-aside>
    <el-container>
      <el-header class="header">
        <minimalist-header />
      </el-header>
      <el-container class="overflow-auto">
        <el-main class="layout-main">
          <router-view :key="route.path" />
        </el-main>
        <el-footer class="flex flex-col justify-center items-stretch">
          <minimalist-footer />
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<style scoped lang="scss">
.minimalist-layout {
  --el-aside-width: auto;
  --el-menu-icon-width: 16px;
  --el-menu-base-level-padding: 12px;
  --el-menu-item-height: 36px;
  --el-menu-sub-item-height: calc(var(--el-menu-item-height) - 6px);
  .aside {
    // 避免展开/合拢aside后主页面抖动
    min-width: calc(var(--el-menu-icon-width) + var(--el-menu-base-level-padding) * 2);
  }

  .header {
    --el-header-height: 2.5rem;
    @apply flex flex-row items-center;
    border-bottom: solid 1px var(--el-menu-border-color);
  }
  .layout-main {
    overflow: unset;
  }

  .el-footer {
    --el-footer-padding: 0 0.5rem;
    --el-footer-height: 36px;
  }
}
</style>
