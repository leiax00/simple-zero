<template>
  <div class="sz-icon">
    <svg :class="`svg-icon ${className}`" aria-hidden="true">
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

<style lang="scss" scoped>
.sz-icon {
  @apply inline-block h-4 w-4;
}

.svg-icon {
  display: inline-block;
  width: 100%;
  height: 100%;
  fill: currentColor;
  overflow: hidden;
}

.icon-6 {
  @apply w-6 h-6;
}
</style>
