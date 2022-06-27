<template>
  <div class="div-home">
    {{ msg }}
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineOptions({ name: 'Home' })
const msg = ref('This is Home Page')
</script>

<style scoped lang="scss">

</style>
