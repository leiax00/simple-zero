<template>
  <div class="div-home bg-fuchsia-600 text-gray-100">
    {{ msg }}
  </div>
  <el-button v-ripple type="primary">hello</el-button>
  <sz-icon />
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineOptions({ name: 'Home' })
const msg = ref('This is Home Page')
</script>

<style scoped lang="scss">

</style>
