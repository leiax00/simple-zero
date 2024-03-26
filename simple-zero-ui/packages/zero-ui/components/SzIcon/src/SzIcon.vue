<template>
  <div class="sz-icon">
    <svg :class="['svg-icon', className]" aria-hidden="true">
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
  &.active {
    color: var(--el-color-primary);
  }
  .svg-icon {
    @apply inline-block w-full h-full fill-current overflow-hidden;
  }
}
</style>
