<template>
  <el-tabs v-model="data.searchEngin.active" type="border-card">
    <el-tab-pane
      v-for="item in data.searchEngin.enginList"
      :key="item.key"
      :name="item.key"
      :label="item.label"
    >
      <el-input
        v-model="data.searchKey"
        :placeholder="item.placeholder"
        clearable
        @keyup.enter="toSearch(item.uri, data.searchKey)"
      />
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import { searchEngin, toSearch } from '@/components/search/engin'

defineOptions({ name: 'EnginSearch' })

const data = reactive({
  searchEngin,
  searchKey: '',
})
</script>

<style scoped></style>
