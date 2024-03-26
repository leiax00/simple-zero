<template>
  <div class="layout-main w-full h-full">
    <component :is="layout" />
    <el-backtop :bottom="64" :right="24">
      <div>UP</div>
    </el-backtop>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'Layout' })
const layoutName = 'MinimalistLayout'
const layoutPath = `./${layoutName.charAt(0).toLowerCase() + layoutName.slice(1)}/${layoutName}.vue`

const layout = shallowRef(defineAsyncComponent(() => import(layoutPath)))
</script>

<style scoped></style>
