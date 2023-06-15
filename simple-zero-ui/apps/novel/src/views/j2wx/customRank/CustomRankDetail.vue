<script setup lang="ts">
import { computed } from 'vue'
import { isEmptyStr } from '@leiax00/utils'
import { tipMsg } from '@leiax00/zero-ui'
import type { CustomRank, J2RankBook } from '@/common'
import common from '@/common'
import { getDefaultRank, rankList } from '@/views/j2wx/customRank/bean'

defineOptions({ name: 'CustomRankDetail' })
const props = defineProps<{
  id: number
}>()
const { id } = toRefs(props)
const pageData = reactive<{
  selectRank: CustomRank
  selectRankInfo: J2RankBook[]
  newRank: CustomRank
  key: string
  novelId: string
}>({
  selectRank: rankList.value[id.value] || {},
  selectRankInfo: [],
  newRank: getDefaultRank(),
  key: '',
  novelId: '',
})

const onSelectRank = function () {
  if (!pageData.selectRank.id) {
    return
  }
  pageData.selectRankInfo = []
  common.apis.getJ2wxCustomRankInfo(pageData.selectRank.id).then((resp) => {
    pageData.selectRankInfo = resp.data
  })
}

const saveRank = () => {
  common.apis.createCustomRank(pageData.newRank as CustomRank).then((resp) => {
    let [message, type] = [`新增榜单: ${pageData.newRank.name} 失败!`, 'error']
    if (resp.code === 0) {
      ;[message, type] = [`新增榜单: ${pageData.newRank.name} 成功!`, 'success']
      const rank = resp.data as CustomRank
      rankList.value[rank.id || 'default'] = rank
      pageData.newRank = getDefaultRank()
    }
    tipMsg(message, type)
  })
}

const loadRank = () => {
  if (isEmptyStr(pageData.key)) {
    return
  }

  common.apis.loadCustomRankByKey(pageData.key).then((resp) => {
    let [message, type] = ['', 'success']
    if (resp.code !== 0) {
      ;[message, type] = ['添加的榜单可能不存在, 请确认秘钥正确!', 'error']
    } else {
      const rank = resp.data as CustomRank
      rankList.value[rank.id || 'default'] = rank
      message = `已添加榜单: ${rank.name}`
    }
    tipMsg(message, type)
  })
}

const removeRank = () => {
  if (isEmptyStr(pageData.key)) {
    return
  }

  const rank = Object.values(rankList.value).find((item) => item.password === pageData.key) as CustomRank
  common.apis.deleteCustomRank(rank.id || 0).then((resp) => {
    let [message, type] = ['', 'success']
    if (resp.code !== 0) {
      ;[message, type] = [`移除榜单: ${rank.name} 失败!`, 'error']
    } else {
      rankList.value = Object.fromEntries(
        Object.keys(rankList.value)
          .filter((item) => item !== `${rank.id}`)
          .map((key) => [key, rankList.value[key]])
      )
      message = `移除榜单: ${rank.name} 成功!`
    }
    tipMsg(message, type)
  })
}

const addNovel = () => {
  if (isEmptyStr(pageData.novelId)) {
    return
  }
  const selectRankId = pageData.selectRank.id as number
  common.apis.addNovel2CustomRank(selectRankId, pageData.novelId.split(',')).then((resp) => {
    let [message, type] = [`添加书籍失败!`, 'error']
    if (resp.code === 0) {
      ;[message, type] = ['添加书籍成功!', 'success']
      pageData.selectRank = resp.data
      rankList.value[selectRankId] = resp.data
      pageData.novelId = ''
      onSelectRank()
    }
    tipMsg(message, type)
  })
}
const delNovel = () => {
  if (isEmptyStr(pageData.novelId)) {
    return
  }
  const selectRankId = pageData.selectRank.id as number
  common.apis.delNovelFromCustomRank(selectRankId, pageData.novelId.split(',')).then((resp) => {
    let [message, type] = [`移除书籍失败!`, 'error']
    if (resp.code === 0) {
      ;[message, type] = ['移除书籍成功!', 'success']
      pageData.selectRank = resp.data
      rankList.value[selectRankId] = resp.data
      pageData.novelId = ''
      onSelectRank()
    }
    tipMsg(message, type)
  })
}

const canSave = computed(() => {
  return !isEmptyStr(pageData.newRank.name) && !isEmptyStr(pageData.newRank.password)
})

onMounted(() => {
  onSelectRank()
})
</script>

<template>
  <div class="main-detail">
    <div class="item menu-wrapper overflow-auto">
      <small-screen-collapse text="折叠/展开操作列表">
        <div class="cur-rank-wrapper">
          <div class="label select-label">选中Rank榜单</div>
          <el-select
            v-model="pageData.selectRank"
            value-key="id"
            filterable
            class="w-full"
            placeholder="请选择榜单"
            @change="onSelectRank"
          >
            <el-option v-for="item in rankList" :key="item.id" :label="item.name" :value="item">
              <span class="float-left">{{ item.name }}</span>
              <span class="float-right text-red-300">{{ item.password }}</span>
            </el-option>
          </el-select>
        </div>
        <el-divider />
        <div class="add-novel-wrapper">
          <div class="label add-label">添加/移除书籍</div>
          <div class="form-wrapper">
            <el-form v-model="pageData.novelId" label-position="top">
              <el-form-item label="书籍ID" prop="novelId">
                <el-input v-model="pageData.novelId" />
              </el-form-item>
              <el-form-item class="form-btn-wrapper">
                <el-button-group class="w-full">
                  <el-button type="primary" class="w-1/2" @click="addNovel">新增书籍</el-button>
                  <el-button type="primary" class="w-1/2" @click="delNovel">移除书籍</el-button>
                </el-button-group>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <el-divider />
        <div class="new-rank-wrapper">
          <div class="label new-label">新增榜单</div>
          <div class="form-wrapper">
            <el-form v-model="pageData.newRank" label-position="top">
              <el-form-item label="Rank 秘钥" prop="password">
                <el-input v-model="pageData.newRank.password" />
              </el-form-item>
              <el-form-item label="Rank 名称" prop="name">
                <el-input v-model="pageData.newRank.name" />
              </el-form-item>
              <el-form-item label="Rank 说明" prop="desc">
                <el-input v-model="pageData.newRank.desc" type="textarea" resize="none" :rows="3" />
              </el-form-item>
              <el-form-item class="form-btn-wrapper">
                <el-button type="primary" class="w-full" :disabled="!canSave" @click="saveRank">新增榜单</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <el-divider />
        <div class="load-rank-wrapper">
          <div class="label new-label">加载/移除榜单</div>
          <div class="form-wrapper">
            <el-form v-model="pageData.key" label-position="top">
              <el-form-item label="Rank 秘钥" prop="key">
                <el-input v-model="pageData.key" />
              </el-form-item>
              <el-form-item class="form-btn-wrapper">
                <el-button-group class="w-full">
                  <el-button type="primary" class="w-1/2" @click="loadRank">加载榜单</el-button>
                  <el-button type="primary" class="w-1/2" @click="removeRank">移除榜单</el-button>
                </el-button-group>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </small-screen-collapse>
    </div>
    <div class="item table-wrapper">
      <div class="table-title">{{ `榜单: ${pageData.selectRank.name || '未选择'}` }}</div>
      <j2wx-rank-table :table-data="pageData.selectRankInfo" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.main-detail {
  @apply flex flex-col gap-8 md:flex-row;
  .item {
    @apply border border-solid p-6 rounded-lg;
    .label {
      @apply mb-3 font-bold;
    }
    &.menu-wrapper {
      @apply lg:w-sz-360;
    }
    &.table-wrapper {
      @apply flex-grow min-w-0;
      .table-title {
        @apply text-center font-bold text-lg lg:text-xl mb-8;
      }
    }
  }
}
</style>
