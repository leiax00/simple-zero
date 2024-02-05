<template>
  <div>
    <div class="relative float-end top-3 right-5 z-10 text-gray-600 text-xs">Ctrl+K / Ctrl+Alt+K</div>
    <el-tabs v-model="data.searchEngin.active" type="border-card" @tab-change="focusInput(enginIndex)">
      <el-tab-pane v-for="item in data.searchEngin.enginList" :key="item.key" :name="item.key" :label="item.label">
        <el-input
          ref="search"
          v-model="data.searchKey"
          :placeholder="item.placeholder"
          clearable
          @keyup.enter="toSearch(item.uri, data.searchKey)"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useMagicKeys } from '@vueuse/core'
import type { InputInstance } from 'element-plus'
import type { Engin } from '@/beans/engin'
import { useApp } from '@/store/app'
import { searchEngin, toSearch } from '@/components/search/engin'

defineOptions({ name: 'EnginSearch' })

const search = ref(null)

const appStore = useApp()

const data = reactive({
  searchEngin,
  searchKey: '',
})

const enginIndex = computed(() =>
  data.searchEngin.enginList.findIndex((item: Engin) => item.key === searchEngin.value.active)
)
const changeSearchEngin = function (reverse = false) {
  const index = enginIndex.value
  let newIndex = index === -1 ? 0 : (index + 1) % data.searchEngin.enginList.length
  if (reverse) {
    if (index === -1) {
      newIndex = 0
    } else if (index === 0) {
      newIndex = searchEngin.value.enginList.length - 1
    } else {
      newIndex = index - 1
    }
  }
  data.searchEngin.active = data.searchEngin.enginList[newIndex].key
  focusInput(newIndex)
}

const focusInput = function (index: number | string) {
  nextTick(() => {
    search.value && (search.value[index] as InputInstance).focus()
  })
}

onMounted(() => {
  if (appStore.config.common?.searchEngin) {
    data.searchEngin.enginList = appStore.config.common.searchEngin
  }
  focusInput(enginIndex.value)
})

const { current } = useMagicKeys({
  passive: false,
  onEventFired(e) {
    if (e.ctrlKey && e.key === 'k') {
      e.preventDefault()
    }
  },
})
watch(current, (v) => {
  if (v.has('control') && v.has('k')) {
    changeSearchEngin(v.has('alt'))
  }
})
</script>

<style scoped></style>
