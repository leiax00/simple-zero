<template>
  <div class="sz-icon">
    <svg :class="`inline-block w-full h-full fill-current overflow-hidden ${className}`" aria-hidden="true">
      <use :xlink:href="iconName" />
    </svg>
  </div>
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

<style lang="scss" scoped></style>
