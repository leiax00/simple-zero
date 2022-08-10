<template>
  <svg :class="`svg-icon ${className}`" aria-hidden="true">
    <use :xlink:href="iconName" />
  </svg>
</template>

<script setup lang="ts">
import { computed, onMounted, toRefs } from 'vue'
import { useApp } from '@/store/app'

defineOptions({ name: 'UvIcon' })
const props = defineProps({
  iconClass: {
    type: String,
    required: true
  },
  className: {
    type: String,
    default: ''
  }
})
const appStore = useApp()

const { iconClass, className } = toRefs(props)
const iconName = computed(() => `#sz-${iconClass.value}`)
onMounted(async () => {
  await appStore.loadSvgSrc()
})
</script>

<style scoped>
.svg-icon {
  display: inline-block;
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
  fill: currentColor;
  overflow: hidden;
}

</style>
