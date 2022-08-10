<template>
  <div class="layout-main">
    <common-layout />
    <!--    <little-cute />-->
    <div class="ctl-bar">
      <el-backtop :bottom="100">
        <div>UP</div>
      </el-backtop>
    </div>
  </div>
</template>

<script setup>
import Sidecar from 'gitter-sidecar/dist/sidecar-module'
import CommonLayout from '@/components/layout/CommonLayout/index.vue'
// import LittleCute from '@/components/LittleCute'

// eslint-disable-next-line no-unused-vars
const sidecar = new Sidecar({
  room: 'exploding-universe/universe'
})
</script>

<style lang="scss" scoped>
.layout-main {

}

</style>
