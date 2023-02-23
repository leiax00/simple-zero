<template>
  <common-skeleton :loading="pageData.loading" class="j2wx-channel">
    <div class="j2wx-channel">
      <div class="title mb-6">J2wx-{{ channel.name }}观测站</div>
      <div class="channel-content">
        <el-collapse
          v-model="pageData.rankCollapse"
          accordion
          class="rank-selector"
        >
          <el-collapse-item name="1">
            <template #title>
              <div class="select-rank" v-html="selectRankShowText" />
            </template>
            <div class="rank-list">
              <el-card
                v-for="(item, index) in pageData.rankList"
                :key="index"
                shadow="never"
                :class="{
                  'rank-item': true,
                  selected: item.id === pageData.selectRank?.id,
                }"
                @click="onSelectRank(item)"
              >
                {{ item.rankName }}
              </el-card>
            </div>
          </el-collapse-item>
        </el-collapse>
        <div v-if="pageData.selectRank" class="data-content mt-6">
          <j2wx-rank-table :table-data="pageData.selectRankInfo" />
        </div>
      </div>
    </div>
  </common-skeleton>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue'
import { storeToRefs } from 'pinia'
import common from '@/common'
import { useServe } from '@/store/serve'
import J2wxRankTable from '@/components/j2wx/J2wxRankTable.vue'

defineOptions({ name: 'J2wxChannel' })

const props = defineProps<{
  channelKey: string
}>()
const serveData = useServe()
const { channelKey } = toRefs(props)
const { getChannel } = storeToRefs(serveData)
const channel = getChannel.value(channelKey.value)

const pageData = reactive<{
  rankList: any[]
  loading: boolean
  selectRank: any
  selectRankInfo: any
  rankCollapse: string
}>({
  rankList: [],
  loading: true,
  selectRank: undefined,
  selectRankInfo: [],
  rankCollapse: '',
})

const collapseRank = (isCollapse: boolean) => {
  pageData.rankCollapse = isCollapse ? '' : '1'
}

const onSelectRank = (item: any) => {
  pageData.selectRank = item
  collapseRank(true)
  pageData.selectRankInfo = []
  common.apis.getJ2wxRankInfo(channelKey.value, item.id).then((resp) => {
    pageData.selectRankInfo = resp.data
  })
}

const selectRankShowText = computed(() => {
  if (pageData.selectRank) {
    return `已选择榜单: <b>${pageData.selectRank.rankName}</b>`
  }
  return '请选择要观测的榜单'
})

onMounted(() => {
  common.apis.getJ2wxRankList(channelKey.value).then((resp) => {
    pageData.rankList = resp.data
    pageData.loading = false
  })
})
</script>

<style scoped lang="scss">
.j2wx-channel {
  @apply p-4;
  .rank-list {
    @apply grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-6 justify-items-center;
    @apply gap-4 sm:gap-x-8 md:gap-x-12 lg:gap-x-16;
    @apply w-full mx-auto;
    .el-card {
      @apply text-center w-full box-border;
      &.rank-item {
        &.selected {
          @apply bg-emerald-400;
        }
      }
    }
  }
}
</style>
