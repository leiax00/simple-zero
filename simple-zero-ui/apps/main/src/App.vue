<template>
  <el-skeleton
    :animated="true"
    :loading="pageData.skeleton.loading"
    :throttle="pageData.skeleton.throttle"
  >
    <template #template>
      <div>loading</div>
    </template>
    <template #default>
      <router-view />
    </template>
  </el-skeleton>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { loadAppConf } from '@/config'
import { updateRouterByServes } from '@/router'
import { useAppCtlStore } from '@/store/app'

const pageData = reactive({
  skeleton: {
    loading: true,
    throttle: 0,
  },
})

const route = useRoute()
onMounted(() => {
  loadAppConf().then((conf: any) => {
    updateRouterByServes(conf.serves || [])
    const appConf = useAppCtlStore()
    appConf.setConfig(conf)
    pageData.skeleton.loading = false
  })
})
</script>
