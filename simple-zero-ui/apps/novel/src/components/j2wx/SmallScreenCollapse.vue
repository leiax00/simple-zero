<script setup lang="ts">
import { computed } from 'vue'

defineOptions({ name: 'SmallScreenCollapse' })
const props = defineProps({
  text: {
    type: String,
    required: true,
  },
})
const { text } = toRefs(props)
const showCollapse = ref(false)

const onClick = () => {
  showCollapse.value = !showCollapse.value
}

const iconClazz = computed(() => {
  return showCollapse.value ? 'rotate-0 -rotated-180' : 'rotate-180 rotated-180'
})

const contentClazz = computed(() => {
  return showCollapse.value ? 'mt-6 md:mt-0 block' : 'mt-6 md:mt-0 hidden md:block'
})
</script>

<template>
  <div class="main-collapse">
    <div class="operate-div" @click="onClick">
      <div class="show-text">{{ text }}</div>
      <sz-icon icon-class="toTop" :class="iconClazz" />
    </div>
    <div :class="`content-wrapper ${contentClazz}`">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.main-collapse {
  .operate-div {
    @apply flex justify-between items-center md:hidden;
  }
}
</style>
