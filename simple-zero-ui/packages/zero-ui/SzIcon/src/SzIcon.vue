<template>
  <svg :class="`svg-icon ${className}`" aria-hidden="true">
    <use :xlink:href="iconName" />
  </svg>
</template>

<script setup lang="ts">
import { computed, toRefs } from 'vue'
import { iconProps } from './vars'
import type { IconProps } from './vars'

defineOptions({
  name: 'SzIcon',
})
const props = defineProps(iconProps)

const { iconClass, className } = toRefs<IconProps>(props)
const iconName = computed(() => `#sz-${iconClass?.value}`)
</script>

<style scoped>
.svg-icon {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  fill: currentColor;
  overflow: hidden;
}
</style>
