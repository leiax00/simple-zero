<script setup lang="ts">
import { reactive } from 'vue'
import { useApp } from '@/store/app'

defineOptions({ name: 'MinimalistFooter' })

const appStore = useApp()
const pageData = reactive({
  copyRightSn: appStore.config.common?.copyright,
})
</script>

<template>
  <el-row class="footer-main">
    <el-col class="text-center text-zinc-400 dark:text-zinc-600 text-xs">
      <sz-icon icon-class="aixin-left" />
      <a href="https://beian.miit.gov.cn/" target="_blank" class="footer-text">{{ pageData.copyRightSn }}</a>
      <sz-icon icon-class="aixin-right" />
    </el-col>
  </el-row>
</template>

<style scoped lang="scss">
.footer-main {
  .footer-text {
    @apply mx-2;
  }
}
</style>
