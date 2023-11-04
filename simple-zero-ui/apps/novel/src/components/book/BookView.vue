<template>
  <div class="main-book">
    <div class="flex flex-wrap justify-start items-start space-y-6 sm:flex-nowrap sm:space-y-0">
      <div class="w-sz-150 flex-shrink-0">
        <img class="object-fill" :src="formatImgUrl(bookInfo.book.icon)" :alt="bookInfo.book.name" />
      </div>
      <div class="book-info text-left sm:ml-6 flex-grow">
        <div class="item">
          <div class="font-bold">书籍名称:</div>
          <div class="ml-3">{{ bookInfo.book.name }}</div>
          <el-button type="primary" @click="add2BookList({ book: bookInfo.book })">收藏</el-button>
        </div>
        <div class="item">
          <div class="font-bold">作者:</div>
          <div class="ml-3">{{ bookInfo.book.author }}</div>
        </div>
        <div class="item">
          <div class="font-bold">书籍类型:</div>
          <div class="ml-3">{{ bookInfo.book.type }}</div>
        </div>
        <div class="item">
          <div class="font-bold">最新章节:</div>
          <div class="ml-3">{{ bookInfo.book.latest_chapter }}</div>
        </div>
        <div class="item">
          <div class="font-bold">更新时间:</div>
          <div class="ml-3">{{ bookInfo.book.update_time }}</div>
        </div>
        <div class="item">
          <div class="font-bold">书籍描述:</div>
          <div class="ml-3 block align-top">{{ bookInfo.book.desc }}</div>
        </div>
      </div>
    </div>
    <div class="w-full text-right">
      <el-button-group class="mt-16">
        <el-button type="primary" @click="sort = 'desc'">逆序</el-button>
        <el-button type="primary" @click="sort = 'asc'">正序</el-button>
      </el-button-group>
    </div>
    <div class="catalog-list mt-4">
      <div v-for="(item, index) in catalogList" :key="index" class="catalog-item">
        <span @click="openChapter(item)">{{ item.name }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, toRefs } from 'vue'
import { useRouter } from 'vue-router'
import type { Book, CatalogBase } from '@/views/bean'
import { add2BookList, formatImgUrl } from '@/components/book/bean'

defineOptions({ name: 'BookView' })

const props = defineProps<{
  bookInfo: Book
}>()

const { bookInfo } = toRefs(props)
const sort = ref('desc')
const catalogList = computed(() => {
  const catalogs = JSON.parse(JSON.stringify(bookInfo.value.catalogs))
  return sort.value === 'asc' ? catalogs : catalogs.reverse()
})

const router = useRouter()
const openChapter = ({ bid, cid }: CatalogBase) => {
  router.push({ path: `/chapter/${bid}/${cid}` })
}
</script>

<style lang="scss" scoped>
.main-book {
  .book-info {
    .item {
      & > div {
        @apply inline-block;
      }
    }
  }

  .catalog-list {
    @apply grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4;
    .catalog-item {
      @apply text-left;
      span {
        @apply cursor-pointer;
      }
    }
  }
}
</style>
