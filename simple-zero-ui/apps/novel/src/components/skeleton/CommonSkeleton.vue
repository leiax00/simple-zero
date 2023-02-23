<template>
  <el-skeleton :animated="true" :loading="loading" :throttle="throttle">
    <template #template>
      <slot name="skeleton">
        <div class="h-full flex justify-center items-center">
          loading{{ new Array(pageData.pointCount).fill('.').join('') }}
        </div>
      </slot>
    </template>
    <template #default>
      <slot />
    </template>
  </el-skeleton>
</template>

<script setup lang="ts">
import { onMounted, reactive, toRefs } from 'vue'

defineOptions({ name: 'CommonSkeleton' })
const props = defineProps({
  loading: {
    type: Boolean,
    required: true,
  },
  throttle: {
    type: Number,
    default: 0,
  },
})
const { loading, throttle } = toRefs(props)
const pageData = reactive({ pointCount: 0 })
onMounted(() => {
  setInterval(() => {
    pageData.pointCount = pageData.pointCount >= 3 ? 0 : pageData.pointCount + 1
  }, 500)
})
</script>

<style scoped></style>
