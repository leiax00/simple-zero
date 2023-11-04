<template>
  <div class="main-book-list">
    <el-skeleton :loading="pageData.loading" animated class="main-skeleton">
      <template #template>
        <div v-for="item in 6" :key="item">
          <el-skeleton-item variant="image" class="skeleton-w" />
          <div style="padding: 14px">
            <el-skeleton-item variant="h3" style="width: 50%" />
          </div>
        </div>
      </template>
      <div class="book-list-wrapper">
        <div
          v-for="[key, novel] in Object.entries(pageData.novelManager.novels)"
          :key="key"
          class="book-item"
          @click="openNovel(novel as Novel)"
        >
          <div class="book-item-logo w-sz-160 h-sz-212">
            <img class="object-fill" :src="formatImgUrl(novel.book.icon)" :alt="novel.book.name" width="150" />
          </div>
          <div class="book-item-text">{{ novel.book.name }}</div>
        </div>
      </div>
    </el-skeleton>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTimeoutFn } from '@vueuse/core'
import { Novel, formatImgUrl, novelManager } from '@/components/book/bean'
import { useApp } from '@/store/app'

defineOptions({
  name: 'BookList',
})

const router = useRouter()
const appStore = useApp()

const pageData = reactive({
  loading: true,
  novelManager,
})

const { start } = useTimeoutFn(() => {
  if (Object.keys(pageData.novelManager.novels).length > 0) {
    pageData.loading = false
  }
}, 1000)

onMounted(() => {
  start()
})

const openNovel = function (novel: Novel) {
  const routeData = {
    bid: novel.book.bid,
    cid: novel.readProgress ? novel.readProgress.cid : novel.book.latest_chapter,
    pos: novel.readProgress ? novel.readProgress.pos : { curPos: 0 },
  }
  appStore.setRouteData(routeData)
  router.push({ path: `/chapter/${routeData.bid}/${routeData.cid}` })
}
</script>

<style scoped lang="scss">
.main-book-list {
  .main-skeleton {
    @apply common-grid;
  }

  .skeleton-w {
    @apply w-sz-160 h-sz-212;
  }
  .book-list-wrapper {
    @apply common-grid;
    .book-item {
      @apply cursor-pointer;
    }
  }
}
</style>
