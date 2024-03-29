<template>
  <common-skeleton :loading="pageData.loading" class="j2wx-channel">
    <div class="j2wx-channel">
      <div class="title mb-6">J2wx-{{ channel.name }}观测站</div>
      <div class="channel-content">
        <el-collapse v-model="pageData.rankCollapse" accordion class="rank-selector">
          <el-collapse-item name="1">
            <template #title>
              <div class="select-rank mr-2">当前榜单:</div>
              <el-select
                v-model="pageData.selectRank"
                :placeholder="selectRankShowText"
                value-key="rankId"
                filterable
                @change="onSelectRank"
              >
                <el-option v-for="item in pageData.rankList" :key="item.rankId" :label="item.rankName" :value="item" />
              </el-select>
            </template>
            <div class="rank-list">
              <el-card
                v-for="(item, index) in pageData.rankList"
                :key="index"
                shadow="never"
                :class="{
                  'rank-item': true,
                  selected: item.rankId === pageData.selectRank?.rankId,
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
import { useSorted } from '@vueuse/core'
import type { J2Rank, J2RankBook } from '@/common'
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
  rankList: J2Rank[]
  loading: boolean
  selectRank?: J2Rank
  selectRankInfo: J2RankBook[]
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
  common.apis.getJ2wxRankInfo(channelKey.value, item.rankId).then((resp) => {
    pageData.selectRankInfo = resp.data
  })
}

const rankListOpts = computed(() => {
  return pageData.rankList.map((item) => ({
    label: item.rankName,
    value: item,
  }))
})

const selectRankShowText = computed(() => {
  if (pageData.selectRank) {
    return `已选择榜单: <b>${pageData.selectRank.rankName}</b>`
  }
  return '请选择要观测的榜单'
})

onMounted(() => {
  common.apis.getJ2wxRankList(channelKey.value).then((resp) => {
    pageData.rankList = useSorted(resp.data as J2Rank[], (a, b) => {
      // xxx.zz, xxx(yy.zz), xxx(yy) 三种情况, 以xxx排序
      return a.rankName.split(/[(.]/)[0] >= b.rankName.split(/[(.]/)[0] ? -1 : 1
    }).value
    pageData.loading = false
  })
})
</script>

<style scoped lang="scss">
.j2wx-channel {
  @apply p-4;
  .rank-list {
    @apply common-grid;
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
