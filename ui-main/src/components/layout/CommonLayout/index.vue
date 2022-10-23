<template>
  <el-container class="common-layout">
    <el-header class="layout-header">
      <common-header />
    </el-header>
    <div class="flex mx-auto md:w-full xl:w-11/12 2xl:w-3/4">
      <!--      <el-aside>-->
      <!--        <common-aside />-->
      <!--      </el-aside>-->
      <el-container class="layout-content">
        <el-main>
          <router-view />
        </el-main>
        <el-footer>
          <common-footer />
        </el-footer>
      </el-container>
    </div>
  </el-container>
</template>

<script setup lang="ts">
import CommonHeader from '@/components/layout/CommonLayout/CommonHeader.vue'
// import CommonAside from '@/components/layout/CommonLayout/CommonAside.vue'
import CommonFooter from '@/components/layout/CommonLayout/CommonFooter.vue'

defineOptions({ name: 'CommonLayout' })

</script>

<style lang="scss" scoped>
$headerH: 4rem;
.layout-header {
  height: $headerH;
}
.layout-content {
  min-height: calc(100vh - #{$headerH} - 12px); // 去除header + 底部的gap
}
</style>
