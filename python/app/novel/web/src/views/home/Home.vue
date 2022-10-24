<template>
  <el-row class="main-novel">
    <el-col :span="24" class="search">
      <el-input
        v-model="pageData.searchVal"
        placeholder="Come on, Baby! 书名搞起"
        class="search-input rounded-2xl"
        @keyup.enter="searchBook"
      />
    </el-col>
    <el-col v-if="pageData.rst" :span="24" class="search-book mt-24 text-center">
      <book-info :book-info="pageData.rst" />
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { reactive, UnwrapNestedRefs } from 'vue'
import common from '@/common'
import BookInfo from '@/views/home/BookInfo.vue'

defineOptions({ name: 'Home' })
const pageData: UnwrapNestedRefs<{
  searchVal: String,
  rst: BookInfo
}> = reactive({
  searchVal: '择日飞升',
  rst: undefined
})

const searchBook = function () {
  common.apis.searchBookByName(pageData.searchVal).then(resp => {
    pageData.rst = resp.data
    console.log(pageData.rst)
  })
}
</script>

<style lang="scss" scoped>
.main-novel {
  .search {
    @apply text-center;
    .search-input{
      width: 500px;
    }
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
