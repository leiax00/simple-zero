<template>
  <el-row class="uv-footer">
    <el-col :span="24">
      <a class="nav-item" href="/"><img :src="logoUrl" alt="Simple Zero" class="h-7"></a>
    </el-col>
    <el-col :span="24">
      <uv-icon icon-class="copyright" />
      <span class="footer-text">{{ `${new Date().getFullYear()} ${pageData.copyright}` }}</span>
    </el-col>
    <el-col :span="24">
      <uv-icon icon-class="copyright" />
      <span class="footer-text">{{ pageData.selfCopyright }}</span>
    </el-col>
    <el-col :span="24">
      <div v-if="pageData.runInfo !== ''">
        <uv-icon icon-class="aixin-left" />
        <span class="footer-text">{{ pageData.runInfo }}</span>
        <uv-icon icon-class="aixin-right" />
      </div>
    </el-col>
    <el-col v-if="pageData.copyRightSn" :span="24">
      <uv-icon icon-class="aixin-left" />
      <a href="https://beian.miit.gov.cn/" target="_blank" class="footer-text">{{ pageData.copyRightSn }}</a>
      <uv-icon icon-class="aixin-right" />
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { useApp } from '@/store/app'

import { onMounted, reactive } from 'vue'
import { useIntervalFn } from '@vueuse/core'
import constObj from '@/bean/constObj'
import timeUtils from '@/utils/timeUtils'
import UvIcon from '@/components/basic/UvIcon/index.vue'

defineOptions({ name: 'CommonFooter' })
const appStore = useApp()
const logoUrl = appStore.logoUrl
const firstRun = appStore.config.app.firstRun
const pageData = reactive({
  copyRightSn: appStore.config.app.copyright,
  copyright: 'Lei.AoX Powered by JcTec',
  selfCopyright: '版权说明：[本网站所有内容均收集于互联网或自己创作,方便于网友与自己学习交流，如有侵权，请留言，立即处理]',
  runInfo: '',
  thanks: '感谢小伙伴的光临!'
})

const refreshRunInfo = function () {
  useIntervalFn(() => {
    const diff = timeUtils.calcTimeDiff(firstRun)
    diff.time = firstRun.split(/[\vt]/ig)[0]
    pageData.runInfo = `本站自 ${diff.time} 已运行 ${diff.day} 天 ${diff.hour} 小时 ${diff.minute} 分 ${diff.second} 秒!`
  }, constObj.TIME_UNIT.ONE_SECOND)
}

onMounted(refreshRunInfo)
</script>
<style lang="scss" scoped>
.footer-text {
  @apply mx-2;
}
</style>
