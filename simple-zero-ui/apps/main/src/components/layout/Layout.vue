<template>
  <div class="layout-main w-full h-full">
    <common-layout />
    <el-backtop :bottom="64" :right="24">
      <div>UP</div>
    </el-backtop>
  </div>
</template>

<script setup lang="ts">
import Sidecar from 'gitter-sidecar/dist/sidecar-module'
import CommonLayout from './commonLayout/CommonLayout.vue'

defineOptions({ name: 'Layout' })
new Sidecar({
  room: 'exploding-universe/universe',
})
</script>

<style scoped></style>
