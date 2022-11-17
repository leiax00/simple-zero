<template>
  <common-title-main>
    <article-title v-if="uiCtl.showArticle" />
  </common-title-main>
</template>

<script setup lang="ts">
import CommonTitleMain from '@/components/layout/CommonLayout/CommonTitle/CommonTitleMain.vue'
import ArticleTitle from '@/components/layout/CommonLayout/CommonTitle/ArticleTitle.vue'
import { useApp } from '@/store/app'

defineOptions({ name: 'CommonTitle' })
const { uiCtl } = useApp()
</script>

<style scoped></style>
