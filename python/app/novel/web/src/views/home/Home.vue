<template>
  <el-row class="main-novel">
    <el-col :span="24" class="search">
      <el-input
        v-model="pageData.searchVal"
        placeholder="Come on, Baby! 书名搞起"
        class="w-full rounded-2xl sm:w-sz-500"
        @keyup.enter="searchBook"
      />
      <el-button v-ripple type="primary" class="mt-3 sm:mt-0 sm:ml-3" @click="searchBook">搜索</el-button>
    </el-col>
    <el-col v-if="pageData.rst" :span="24" class="search-book mt-24 text-center">
      <book-view :book-info="pageData.rst" />
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { reactive, UnwrapNestedRefs } from 'vue'
import common from '@/common'
import BookView from '@/views/home/BookView.vue'
import { defineOptions } from 'unplugin-vue-define-options/macros'
import { Book } from '@/views/bean'

defineOptions({ name: 'Home' })
const pageData: UnwrapNestedRefs<{
  searchVal: String,
  rst?: Book
}> = reactive({
  searchVal: '择日飞升',
  rst: undefined
})

const searchBook = function () {
  common.apis.searchBookByName(pageData.searchVal).then(resp => {
    pageData.rst = resp.data
  })
}
</script>

<style lang="scss" scoped>
.main-novel {
  .search {
    @apply text-center;
  }
  :deep(.el-input) {
    .el-input__wrapper {
      @apply rounded-2xl;
      .el-input__inner {

      }
    }
  }

}
</style>
