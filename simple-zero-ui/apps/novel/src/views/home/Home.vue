<template>
  <div class="main-novel">
    <div class="search">
      <el-input
        v-model="pageData.searchVal"
        placeholder="Come on, Baby! 书名搞起"
        class="search-input"
        @keyup.enter="searchBook"
      />
      <el-button
        v-ripple
        type="primary"
        class="mt-3 sm:mt-0 sm:ml-3"
        @click="searchBook"
        >搜索</el-button
      >
    </div>
    <div class="search-book mt-8 text-center flex-grow">
      <book-view v-if="pageData.rst" :book-info="pageData.rst" />
      <book-list v-else />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { UnwrapNestedRefs } from 'vue'
import type { Book } from '@/views/bean'
import common from '@/common'

defineOptions({ name: 'Home' })
const pageData: UnwrapNestedRefs<{
  searchVal: string
  rst?: Book
}> = reactive({
  searchVal: '择日飞升',
  rst: undefined,
})

const searchBook = function () {
  common.apis.searchBookByName(pageData.searchVal).then((resp) => {
    pageData.rst = resp.data
  })
}
</script>

<style lang="scss" scoped>
.main-novel {
  @apply h-full flex flex-col flex-nowrap p-4;
  .search {
    @apply text-center;
    .search-input {
      @apply w-full rounded-2xl sm:w-sz-500;
    }
  }
  :deep(.el-input) {
    .el-input__wrapper {
      @apply rounded-2xl;
      .el-input__inner {
      }
    }
  }

  .book-list {
    @apply mt-8 text-center;
  }
}
</style>
