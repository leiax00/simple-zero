<template>
  <div>{{ $route.path }}</div>
  <router-view :key="routePath" />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

defineOptions({ name: 'Layout' })
const routePath = computed(() => useRoute().path)

</script>

<style scoped>

</style>
