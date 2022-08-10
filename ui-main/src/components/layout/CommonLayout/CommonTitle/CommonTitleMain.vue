<template>
  <div class="title-detail-wrapper">
    <slot>
      <h1 class="text-h1">Simple Zero</h1>
      <div class="sub-title text-h4">Everything will be better</div>
    </slot>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'CommonTitleMain' })
</script>

<style lang="scss" scoped>
.title-detail-wrapper {
  @apply w-full mx-auto py-40 text-center;
  @apply text-gray-300;
  //@apply text-teal-500;
  .text-h1 {
    @apply text-5xl py-4;
  }
  .text-h4 {
    @apply text-3xl;
  }
}
</style>
