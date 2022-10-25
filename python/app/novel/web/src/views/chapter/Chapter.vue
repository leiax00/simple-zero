<template>
  <div class="main-chapter">
    <div class="chapter-name">{{ pageData.chapter.name }}</div>
    <div class="chapter-text" v-html="chapterText" />
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, toRefs } from 'vue'
import common from '@/common'
import { Chapter } from '@/views/bean'

defineOptions({ name: 'Chapter' })
const props = defineProps<{
  bid: string,
  cid: string
}>()
const { bid, cid } = toRefs(props)

const pageData = reactive<{chapter: Chapter}>({ chapter: {} })
const chapterText = computed(() => {
  return pageData.chapter.content ? pageData.chapter.content.replaceAll('\n', '<br/>') : ''
})

onMounted(() => {
  common.apis.getChapter(bid.value, cid.value).then(resp => {
    pageData.chapter = resp.data
  })
})

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
  .btn-group {}
}
</style>
