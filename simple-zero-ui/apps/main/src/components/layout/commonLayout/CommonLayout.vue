<template>
  <el-container ref="layout" class="common-layout">
    <Transition name="el-fade-in-linear">
      <el-aside
        v-if="appStore.uiCtl.showAside"
        ref="aside"
        class="sm:hidden aside-main"
      >
        <common-aside />
      </el-aside>
    </Transition>
    <el-container>
      <el-header class="layout-header">
        <common-header />
      </el-header>
      <el-main class="layout-main">
        <router-view :key="route.path" />
      </el-main>
      <el-footer>
        <common-footer />
      </el-footer>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'
import { useRoute } from 'vue-router'
import CommonHeader from '@/components/layout/commonLayout/CommonHeader.vue'
import CommonFooter from '@/components/layout/commonLayout/CommonFooter.vue'
import { useApp } from '@/store/app'
defineOptions({ name: 'CommonLayout' })

const appStore = useApp()
const aside = ref(null)
onClickOutside(aside, () => {
  appStore.uiCtl.showAside = false
})

const route = useRoute()
</script>

<style lang="scss" scoped>
.common-layout {
  @apply h-full;
  .layout-header {
    @apply w-full;
  }
  .layout-main {
    overflow: unset;
  }
  .aside-main {
    @apply absolute z-50 h-full shadow-aside-red-right;
    @apply bg-body;

    &:before {
      @apply absolute;
    }
  }
  .el-footer {
    @apply pb-2;
    height: unset;
  }
}
:deep(.el-scrollbar__view) {
  @apply h-full;
}
</style>
