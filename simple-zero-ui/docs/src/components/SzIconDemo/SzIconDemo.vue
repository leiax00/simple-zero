<template>
  <div class="main-szicon">
    <sz-icon icon-class="copyright" class-name="icon-3" />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'SzIconDemo',
})
</script>

<style lang="scss" scoped>
.main-szicon {
  .icon-3 {
    @apply h-5 w-5;
  }
}
</style>
