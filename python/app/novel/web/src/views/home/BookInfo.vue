<template>
  <el-row :gutter="64" justify="start" class="main-book">
    <el-col :span="6" class="book-icon">
      <img :src="bookInfo.book.icon" :alt="bookInfo.book.name">
      <!--      <div>-->
      <!--      </div>-->
    </el-col>
    <el-col :span="18" class="book-base-info ">
      <div class="item">
        <div class="font-bold">书籍名称: </div>
        <div class="ml-3">{{ bookInfo.book.name }}</div>
      </div>
      <div class="item">
        <div class="font-bold">作者: </div>
        <div class="ml-3">{{ bookInfo.book.author }}</div>
      </div>
      <div class="item">
        <div class="font-bold">书籍类型: </div>
        <div class="ml-3">{{ bookInfo.book.type }}</div>
      </div>
      <div class="item">
        <div class="font-bold">最新章节: </div>
        <div class="ml-3">{{ bookInfo.book.latest_chapter }}</div>
      </div>
      <div class="item">
        <div class="font-bold">更新时间: </div>
        <div class="ml-3">{{ bookInfo.book.update_time }}</div>
      </div>
      <div class="item">
        <div class="font-bold">书籍描述: </div>
        <div class="ml-3 block">{{ bookInfo.book.desc }}</div>
      </div>
    </el-col>
    <el-col :span="24" class="catalog-list-wrapper">
      <div class="catalog-list">
        <div
          v-for="(item, index) in catalogList"
          :key="index"
          class="catalog-item"
        >
          <span @click="openChapter(item)">{{ item.name }}</span>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { BookInfo } from '@/views/home/bean'
import { computed, toRefs } from 'vue'
defineOptions({ name: 'BookInfo' })

const props = defineProps<{
  bookInfo: BookInfo
}>()

const { bookInfo } = toRefs(props)
const catalogList = computed(() => {
  const catalogs = bookInfo.value.catalogs
  return catalogs.reverse()
})

const openChapter = ({ bid, cid }) => {
  console.log(bid, cid)
}

</script>

<style lang="scss" scoped>
.main-book {
  .book-icon {
    @apply text-right;
    text-align: -webkit-right;
    img {
      width: 180px;
    }
  }
  .book-base-info {
    @apply align-top text-left;
    .item {
      &>div {
        @apply inline-block;
      }
    }
  }
  .catalog-list-wrapper {
    @apply mt-16;
    .catalog-list {
      display: flex;
      justify-content: flex-start;
      align-items: center;
      flex-flow: row wrap;
      .catalog-item {
        @apply py-2 px-3 text-left;
        width: 25%;
        span {
          @apply cursor-pointer;
        }
      }
    }

  }
}
</style>
