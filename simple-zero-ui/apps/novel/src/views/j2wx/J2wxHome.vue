<template>
  <div class="j2wx-main">
    <div class="title mb-6">J2wx观测站</div>
    <div class="channel-list">
      <el-card
        v-for="item in channelList"
        :key="item.channelKey"
        v-ripple
        shadow="always"
        :style="toStyles(item)"
        @click="routeTo(item)"
        >{{ item.name }}</el-card
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import colors from 'tailwindcss/colors'
import { useRouter } from 'vue-router'
import { useApp } from '@/store/app'
import { useServe } from '@/store/serve'

defineOptions({ name: 'J2wxHome' })
const router = useRouter()
const serveData = useServe()

const channelList = serveData.j2wx.channelList
const toStyles = (item: { color: string; bgColor: string }) => ({
  color: item.color || colors.black,
  'background-color': item.bgColor || colors.white,
})

const routeTo = (item: { channelKey: string }) => {
  router.push({ path: `/j2wx/channel/${item.channelKey}` })
}
</script>

<style scoped lang="scss">
.j2wx-main {
  @apply p-4;
  .channel-list {
    @apply common-grid;
    .el-card {
      @apply text-center w-full;
    }
  }
}
</style>
