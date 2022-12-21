<template>
  <el-container ref="layout" class="common-layout">
    <el-header :class="headerClazz">
      <common-header />
    </el-header>
    <el-main class="layout-main">
      <div ref="el">Main</div>
    </el-main>
    <el-footer>
      <common-footer />
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, reactive } from 'vue'
import CommonHeader from '@/components/layout/commonLayout/CommonHeader.vue'
import CommonFooter from '@/components/layout/commonLayout/CommonFooter.vue'
defineOptions({ name: 'CommonLayout' })

const navState = reactive({ scrollTop: 0, preScrollTop: 0 })
const headerClazz = computed(() => {
  const needFixed =
    navState.scrollTop < 64 || navState.scrollTop < navState.preScrollTopc
  return {
    'layout-header': true,
    // 往下滚动时, 自动隐藏nav
    'unfixed-top': !needFixed,
  }
})

const handleScroll = function () {
  const curScrollTop =
    document.documentElement.scrollTop || document.body.scrollTop
  if (Math.abs(curScrollTop - navState.scrollTop) > 32) {
    navState.preScrollTop = navState.scrollTop
    navState.scrollTop = curScrollTop
  }
}
document.addEventListener('scroll', handleScroll)
onBeforeUnmount(() => {
  document.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
.common-layout {
  @apply h-full;
  .layout-header {
    @apply top-0 left-0 fixed z-10;
    @apply w-full;
    &.unfixed-top {
      @apply -top-16;
    }
  }
  .layout-main {
    @apply mt-16;
  }
}
</style>
