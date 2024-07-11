<script setup lang="tsx">
import { computed, defineComponent, reactive, toRefs } from 'vue'
import { useDark, useToggle } from '@vueuse/core'

defineOptions({ name: 'ThemeTogglerNew' })

interface Props {
  width?: number
  size?: 'large' | 'default' | 'small'
}
const props = withDefaults(defineProps<Props>(), {
  size: 'default',
  height: 20,
})

const { width, size } = toRefs(props)

const isDark = useDark({
  storageKey: 'theme-appearance',
})

const pageData = reactive({ dark: isDark.value })

const actionSize = computed(() => {
  const map = { large: 16, default: 12, small: 8 }
  return map[size.value]
})

const switchStyles = computed(() => {
  const heightMap = { large: 24, default: 20, small: 16 }
  return {
    height: `${heightMap[size.value]}px`,
  }
})
const toggleDark = useToggle(isDark)

const dark = defineComponent(() => {
  return () => {
    return (
      <el-icon size={actionSize.value}>
        <svg class="dark-icon" viewBox="0 0 24 24">
          <path
            d="M11.01 3.05C6.51 3.54 3 7.36 3 12a9 9 0 0 0 9 9c4.63 0 8.45-3.5 8.95-8c.09-.79-.78-1.42-1.54-.95A5.403 5.403 0 0 1 11.1 7.5c0-1.06.31-2.06.84-2.89c.45-.67-.04-1.63-.93-1.56z"
            fill="currentColor"
          />
        </svg>
      </el-icon>
    )
  }
})

const light = defineComponent(() => {
  return () => {
    return (
      <el-icon size={actionSize.value}>
        <svg class="light-icon" viewBox="0 0 24 24">
          <path
            d="M6.05 4.14l-.39-.39a.993.993 0 0 0-1.4 0l-.01.01a.984.984 0 0 0 0 1.4l.39.39c.39.39 1.01.39 1.4 0l.01-.01a.984.984 0 0 0 0-1.4zM3.01 10.5H1.99c-.55 0-.99.44-.99.99v.01c0 .55.44.99.99.99H3c.56.01 1-.43 1-.98v-.01c0-.56-.44-1-.99-1zm9-9.95H12c-.56 0-1 .44-1 .99v.96c0 .55.44.99.99.99H12c.56.01 1-.43 1-.98v-.97c0-.55-.44-.99-.99-.99zm7.74 3.21c-.39-.39-1.02-.39-1.41-.01l-.39.39a.984.984 0 0 0 0 1.4l.01.01c.39.39 1.02.39 1.4 0l.39-.39a.984.984 0 0 0 0-1.4zm-1.81 15.1l.39.39a.996.996 0 1 0 1.41-1.41l-.39-.39a.993.993 0 0 0-1.4 0c-.4.4-.4 1.02-.01 1.41zM20 11.49v.01c0 .55.44.99.99.99H22c.55 0 .99-.44.99-.99v-.01c0-.55-.44-.99-.99-.99h-1.01c-.55 0-.99.44-.99.99zM12 5.5c-3.31 0-6 2.69-6 6s2.69 6 6 6s6-2.69 6-6s-2.69-6-6-6zm-.01 16.95H12c.55 0 .99-.44.99-.99v-.96c0-.55-.44-.99-.99-.99h-.01c-.55 0-.99.44-.99.99v.96c0 .55.44.99.99.99zm-7.74-3.21c.39.39 1.02.39 1.41 0l.39-.39a.993.993 0 0 0 0-1.4l-.01-.01a.996.996 0 0 0-1.41 0l-.39.39c-.38.4-.38 1.02.01 1.41z"
            fill="currentColor"
          />
        </svg>
      </el-icon>
    )
  }
})
</script>

<template>
  <el-switch
    v-model="pageData.dark"
    :width="width"
    :size="size"
    :active-action-icon="dark"
    :inactive-action-icon="light"
    :style="switchStyles"
    @change="toggleDark"
  />
</template>

<style scoped lang="scss">
.el-switch {
  --el-switch-on-color: var(--el-border-color);
  --el-switch-off-color: var(--el-border-color);
  :deep(.el-switch__core) {
    background: var(--sz-bg-color-mute);
  }

  :deep(.el-switch__core .el-switch__action) {
    background-color: var(--el-bg-color);
    color: var(--text-color-light);
  }
}
</style>
