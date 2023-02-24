<template>
  <div class="rank-expand">
    <div v-for="(item, index) in lineList" :key="index" class="line">
      <div class="line-label">{{ item.label }}:</div>
      <div class="line-val">{{ item.val }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'

defineOptions({ name: 'J2wxRankExpandView' })
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
})

const { data } = toRefs(props)

const lineList = [
  { label: '小说名称', val: data.value.book.name },
  { label: '作者', val: data.value.book.authorName },
  { label: '字数', val: data.value.book.size },
  { label: '标签', val: data.value.book.tags },
  { label: '类型', val: data.value.book.type },
]
</script>

<style scoped lang="scss">
.rank-expand {
  @apply pl-8;
  .line {
    @apply flex flex-row;
    & > div {
      @apply inline-block;
    }
    .line-label {
      @apply pr-2;
    }
    .line-val {
      @apply flex-grow font-bold;
    }
  }
}
</style>
