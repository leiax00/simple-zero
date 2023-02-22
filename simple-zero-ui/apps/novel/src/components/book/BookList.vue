<template>
  <div class="main-book-list">
    <el-skeleton
      v-for="item in 6"
      :key="item"
      class="skeleton-w"
      :loading="loading"
      animated
    >
      <template #template>
        <el-skeleton-item
          variant="image"
          class="skeleton-w"
          style="height: 240px"
        />
        <div style="padding: 14px">
          <el-skeleton-item variant="h3" style="width: 50%" />
        </div>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

defineOptions({
  name: 'BookList',
})
const loading = ref(true)
onMounted(() => {
  console.log('loading book List')
})
</script>

<style scoped lang="scss">
.main-book-list {
  @apply grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-6 justify-items-center;
  @apply gap-4 sm:gap-x-8 md:gap-x-12 lg:gap-x-16;
  @apply w-full md:w-3/4 mx-auto;
  .skeleton-w {
    @apply w-sz-160;
  }
}
</style>
