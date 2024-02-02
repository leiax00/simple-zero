<template>
  <div class="main-chapter">
    <div class="chapter-name">{{ pageData.chapter.name }}</div>
    <div class="chapter-text" v-html="chapterText" />
    <div class="btn-group">
      <el-button type="primary" :disabled="pageData.chapter.prev === -1" @click="openPage(true)"> 上一章 </el-button>
      <el-button type="primary" :disabled="pageData.chapter.next === -1" @click="openPage(false)"> 下一章 </el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useScroll } from '@vueuse/core'
import type { Chapter } from '@/views/bean'
import common from '@/common'
import { calcCurPos, updateReadProgress } from '@/components/book/bean'

defineOptions({ name: 'Chapter' })

const props = defineProps<{
  bid: string
  cid: string
}>()
const { bid, cid } = toRefs(props)

const pageData = reactive<{ chapter: Chapter }>({
  chapter: {
    bid: bid.value,
    cid: cid.value,
    name: cid.value,
    prev: -1,
    next: -1,
    content: '',
  },
  timer: -1,
})
const chapterText = computed(() => {
  return pageData.chapter.content ? pageData.chapter.content.replaceAll('\n', '<br/>') : ''
})

onMounted(() => {
  common.apis.getChapter(bid.value, cid.value).then((resp) => {
    pageData.chapter = resp.data
    nextTick(() => {
      window.scrollTo({
        top: calcCurPos(bid.value),
      })
    })
  })
})

const { y } = useScroll(document)

watch(y, () => {
  updateReadProgress(bid.value, cid.value, Math.floor(y.value - 32))
})

const router = useRouter()
const openPage = (isPrev: boolean) => {
  const routeData = {
    bid: bid.value,
    cid: isPrev ? pageData.chapter.prev : pageData.chapter.next,
  }
  updateReadProgress(routeData.bid, routeData.cid, 0)
  router.push({
    path: `/chapter/${routeData.bid}/${routeData.cid}`,
  })
}
</script>

<style lang="scss" scoped>
.main-chapter {
  .chapter-name {
    @apply text-center font-bold text-2xl py-6;
  }
  .chapter-text {
    @apply mt-6;
    @apply font-normal leading-8;
  }
  .btn-group {
    @apply text-center mt-9;
  }
}
</style>
