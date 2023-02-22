<template>
  <div class="j2wx-channel">
    <div class="title mb-6">J2wx-{{ routeData.name }}观测站</div>
    <div class="channel-content">
      <el-collapse accordion class="rank-selector">
        <el-collapse-item name="1">
          <template #title>
            <div class="select-rank">选择频道: <b>频道金榜</b></div>
          </template>
          <div class="rank-list">Rank list</div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { useApp } from '@/store/app'
import common from '@/common'

defineOptions({ name: 'J2wxChannel' })

const props = defineProps<{
  channelKey: string
}>()
const appConf = useApp()
const { channelKey } = toRefs(props)
const routeData = appConf.routeData
const pageData = reactive({
  rankList: {},
})
onMounted(() => {
  common.apis
    .getJ2wxRankList(channelKey)
    .then((resp) => (pageData.rankList = resp))
})
</script>

<style scoped lang="scss">
.j2wx-channel {
  @apply p-4;
}
</style>
