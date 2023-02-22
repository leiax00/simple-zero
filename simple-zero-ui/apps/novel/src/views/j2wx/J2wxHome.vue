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

defineOptions({ name: 'J2wxHome' })
const router = useRouter()

const channelList = [
  { name: '古代言情', channelKey: 'gywx', color: '', bgColor: '' },
  { name: '都市青春', channelKey: 'dsyq', color: '', bgColor: '' },
  { name: '幻想现言', channelKey: 'qqyq', color: '', bgColor: '' },
  { name: '古代穿越', channelKey: 'gdcy', color: '', bgColor: '' },
  { name: '奇幻言情', channelKey: 'xhqh', color: '', bgColor: '' },
  { name: '未来游戏悬疑', channelKey: 'xywy', color: '', bgColor: '' },
  { name: '都市现纯', channelKey: 'xddm', color: '', bgColor: '' },
  { name: '幻想现纯', channelKey: 'blhx', color: '', bgColor: '' },
  { name: '古代纯爱', channelKey: 'gddm', color: '', bgColor: '' },
  { name: '百合小说', channelKey: 'bhxs', color: '', bgColor: '' },
  { name: '无CP', channelKey: 'nocp', color: '', bgColor: '' },
]
const toStyles = (item: { color: string; bgColor: string }) => ({
  color: item.color || colors.black,
  'background-color': item.bgColor || colors.white,
})

const routeTo = (item: { channelKey: string }) => {
  const appConf = useApp()
  appConf.setRouteData(item)
  router.push({ path: `/j2wx/channel/${item.channelKey}` })
}
</script>

<style scoped lang="scss">
.j2wx-main {
  @apply p-4;
  .channel-list {
    @apply grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-6 justify-items-center;
    @apply gap-4 sm:gap-x-8 md:gap-x-12 lg:gap-x-16;
    @apply w-full lg:w-3/4 mx-auto;
    .el-card {
      @apply text-center w-full;
    }
  }
}
</style>
