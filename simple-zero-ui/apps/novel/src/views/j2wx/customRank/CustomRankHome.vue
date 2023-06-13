<script setup lang="ts">
import { computed } from 'vue'
import { isEmptyStr } from '@leiax00/utils'
import type { CustomRank } from '@/views/j2wx/customRank/bean'
import { TYPE_OPERATE, getDefaultRank, rankList } from '@/views/j2wx/customRank/bean'

defineOptions({ name: 'CustomRank' })
const pageData = reactive<{
  curOperate: string
  newRank: CustomRank
}>({ curOperate: TYPE_OPERATE.SHOW, newRank: getDefaultRank() })

const changeOperate = (operate: string) => {
  pageData.newRank = getDefaultRank()
  pageData.curOperate = operate
}

const saveRank = () => {
  rankList.value[pageData.newRank.id || 'default'] = pageData.newRank as CustomRank
  pageData.curOperate = TYPE_OPERATE.SHOW
}

const router = useRouter()
const selectRank = (rank: CustomRank) => {
  router.push({ path: `/j2wx/rank/${rank.id}` })
}

const addClazz = computed(() => {
  return pageData.curOperate === TYPE_OPERATE.ADD ? 'in-from-right' : 'out-to-right'
})

const showClazz = computed(() => {
  return pageData.curOperate === TYPE_OPERATE.SHOW ? 'in-from-left' : 'out-to-left'
})

const canSave = computed(() => {
  return !isEmptyStr(pageData.newRank.name) && !isEmptyStr(pageData.newRank.password)
})
</script>

<template>
  <div class="main-rank">
    <div class="rank-list-wrapper">
      <div v-if="pageData.curOperate === TYPE_OPERATE.SHOW" :class="`rank-list-show ${showClazz}`">
        <div class="item-wrapper">
          <div v-if="Object.keys(rankList).length === 0" class="no-rank">没有可用的Rank</div>
          <div v-for="item in rankList" :key="item.id" class="rank-item" @click="selectRank(item)">
            {{ item.name }}
          </div>
        </div>
        <el-button-group class="w-full mt-6">
          <el-button type="primary" size="large" class="w-1/2" @click="changeOperate(TYPE_OPERATE.ADD)">新增 Rank</el-button>
          <el-button type="primary" size="large" class="w-1/2" @click="changeOperate(TYPE_OPERATE.LOAD)">加载 Rank</el-button>
        </el-button-group>
      </div>
      <div v-else-if="pageData.curOperate === TYPE_OPERATE.ADD" :class="`add-rank-wrapper ${addClazz}`">
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
            <el-button-group class="w-full">
              <el-button type="primary" class="w-1/2" :disabled="!canSave" @click="saveRank">保存</el-button>
              <el-button type="primary" class="w-1/2" @click="changeOperate(TYPE_OPERATE.SHOW)">返回</el-button>
            </el-button-group>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main-rank {
  @apply flex justify-center items-center;
  min-height: 460px;
  .rank-list-wrapper {
    @apply w-sz-360 rounded-2xl p-8 bg-gray-500 shadow-sz-1 shadow-gray-500 overflow-hidden;
    --el-text-color-regular: theme('colors.gray.200');
    height: 400px;
    :deep(.el-form) {
      --el-text-color-regular: theme('colors.gray.200');
      .el-input,
      .el-textarea {
        --el-input-bg-color: none;
      }
    }

    .rank-list-show {
      @apply w-full h-full flex flex-col justify-center;
      @apply leading-10 text-gray-200;
      .no-rank {
        @apply text-center;
      }
      .rank-item {
        @apply w-full h-10 bg-violet-400;
        @apply px-8;
        @apply hover:bg-violet-500;

        & + .rank-item {
          @apply border-0 border-t border-solid border-gray-500;
        }

        &:first-child {
          @apply rounded-tl-lg rounded-tr-lg;
        }
        &:last-child {
          @apply rounded-bl-lg rounded-br-lg;
        }
      }
    }

    .add-rank-wrapper {
      @apply w-full h-full flex flex-col justify-center;
      .form-btn-wrapper {
        :deep(.el-form-item__content) {
          @apply w-full;
        }
      }
    }
  }
}
</style>
