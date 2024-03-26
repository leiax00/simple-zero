<script setup lang="ts">
import { onMounted } from 'vue'
import TypeIt from 'typeit'
import { getYiYan } from '@leiax00/zero-ui/api'

defineOptions({ name: 'MinimalistHeader' })

const router = useRouter()
const toHome = () => {
  router.push('/')
}
const homeClazz = computed(() => {
  const tmp = ['cursor-pointer w-5 h-5']
  if (router.currentRoute.value.path === '/home') {
    tmp.push('active')
  }
  return tmp
})

let writer: any = null
const runTypeWriterInstance = (text: string) => {
  if (!writer) {
    writer = new TypeIt('.type-writer', { speed: 100 })
  }
  writer.type(text)
  writer.go()
}
onMounted(() => {
  getYiYan({ c: 'k' }).then((resp) => {
    console.log(resp, resp.hitokoto)
    const { hitokoto, from, from_who: author } = resp
    const text = `
<div class="">${hitokoto}</div>
`
    runTypeWriterInstance(text)
  })
})
</script>

<template>
  <el-row class="head-main w-full items-center">
    <el-col :sm="8" :span="12">
      <sz-icon icon-class="home" :class="homeClazz" title="首页" @click="toHome" />
    </el-col>
    <el-col :sm="8" class="text-center hidden sm:block">
      <div class="type-writer flex justify-center text-zinc-500 text-xs" />
    </el-col>
    <el-col :sm="8" :span="12" class="header-right">
      <sz-theme-toggler-new />
      <avatar icon-clazz="icon-5" />
    </el-col>
  </el-row>
</template>

<style scoped lang="scss">
.head-main {
  .header-right {
    @apply flex flex-row justify-end items-center;
    & > div {
      @apply align-middle;
      & + div {
        @apply ml-4;
      }
    }
  }
  :deep(.ti-cursor) {
    display: none;
  }
}
</style>
