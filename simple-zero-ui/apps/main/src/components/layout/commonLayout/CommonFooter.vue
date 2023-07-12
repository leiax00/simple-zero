<template>
  <el-row class="layout-footer">
    <el-col :span="24">
      <a class="nav-item inline-block" href="/">
        <img :src="logoUrl" alt="Simple Zero" class="h-7" />
      </a>
    </el-col>
    <el-col :span="24">
      <sz-icon icon-class="copyright" class="icon-3" />
      <span class="footer-text">{{ `${new Date().getFullYear()} ${pageData.copyright}` }}</span>
    </el-col>
    <el-col :span="24">
      <sz-icon icon-class="copyright" class="icon-3" />
      <span class="footer-text">{{ pageData.selfCopyright }}</span>
    </el-col>
    <el-col :span="24">
      <div v-if="pageData.runInfo !== ''">
        <sz-icon icon-class="aixin-left" />
        <span class="footer-text">{{ pageData.runInfo }}</span>
        <sz-icon icon-class="aixin-right" />
      </div>
    </el-col>
    <el-col v-if="pageData.copyRightSn" :span="24">
      <sz-icon icon-class="aixin-left" />
      <a href="https://beian.miit.gov.cn/" target="_blank" class="footer-text">{{ pageData.copyRightSn }}</a>
      <sz-icon icon-class="aixin-right" />
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { onMounted, reactive } from 'vue'
import { useIntervalFn } from '@vueuse/core'
import { useApp } from '@/store/app'

defineOptions({
  name: 'CommonFooter',
})
const appStore = useApp()
const logoUrl = appStore.logoUrl
const pageData = reactive({
  firstRun: appStore.config.common?.firstRun,
  copyRightSn: appStore.config.common?.copyright,
  copyright: 'Lei.AoX Powered by JcTec',
  selfCopyright:
    '版权说明：[本网站所有内容均收集于互联网或自己创作,方便于网友与自己学习交流，如有侵权，请留言，立即处理]',
  runInfo: '',
  thanks: '感谢小伙伴的光临!',
})

const refreshRunInfo = function () {
  useIntervalFn(() => {
    // const diff = timeUtils.calcTimeDiff(firstRun)
    // diff.time = pageData.firstRun.split(/[\vt]/gi)[0]
    // pageData.runInfo = `本站自 ${diff.time} 已运行 ${diff.day} 天 ${diff.hour} 小时 ${diff.minute} 分 ${diff.second} 秒!`
  }, 1000)
}

onMounted(refreshRunInfo)
</script>

<style lang="scss" scoped>
.layout-footer {
  @apply font-light text-xs text-gray-500 italic;
  .footer-text {
    @apply mx-2;
  }
  .icon-3 {
    @apply h-3 w-3;
  }
}
</style>
