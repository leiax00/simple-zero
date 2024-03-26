<script setup lang="ts">
import { onClickOutside, useMagicKeys, useWindowSize } from '@vueuse/core'
import { breakpoints, breakpointsTailwind } from '@leiax00/constants'
import { Document, Menu as IconMenu, Location, Setting } from '@element-plus/icons-vue'
import { useApp } from '@/store/app'

defineOptions({ name: 'MinimalistAside' })
const { logoUrl } = useApp()

const isCollapse = ref(true)
// aside是否脱离文档流, 最大程度保证页面布局不变动(仅收起状态的侧边栏占位)
const asideFloat = ref(true)

const handleSelect = (index: string, indexPath: string[]) => {
  console.log(index, indexPath)
}

const asideClazz = reactive<Record<any, any>>({
  'aside-main--collapse': isCollapse.value,
  relative: isCollapse.value,
  fixed: !isCollapse.value,
})

watch(isCollapse, () => {
  asideClazz['aside-main--collapse'] = isCollapse.value
  if (asideFloat.value && !isCollapse.value) {
    asideClazz['relative'] = false
    asideClazz['fixed z-10 lg:relative'] = true
  }

  setTimeout(() => {
    if (asideFloat.value && isCollapse.value) {
      asideClazz['relative'] = true
      asideClazz['fixed z-10 lg:relative'] = false
    }
  }, 300) // --el-transition-duration
})

const { width } = useWindowSize()
const aside = ref(null)
onClickOutside(aside, () => {
  if (width.value < breakpointsTailwind.lg) {
    isCollapse.value = true
  }
})

const { ctrl, '`': bracketLeft } = useMagicKeys()
watchEffect(() => {
  if (ctrl.value && bracketLeft.value) {
    isCollapse.value = !isCollapse.value
  }
})
</script>

<template>
  <div ref="aside" :class="{ 'aside-main': true, ...asideClazz }">
    <div class="aside-header" @click="() => (isCollapse = !isCollapse)">
      <div class="logo-wrapper h-16 flex flex-row items-center pl-3" title="显示/隐藏侧边栏Ctrl+`">
        <span class="logo contents">
          <img v-if="isCollapse" src="https://static.leiax00.cn/dev/pics/logo-sz.png" alt="Simple Zero" class="w-4" />
          <img v-else :src="logoUrl" alt="Simple Zero" class="w-32" />
        </span>
      </div>
    </div>
    <el-menu
      default-active="2"
      :collapse-transition="false"
      :style="{ 'min-height': 'calc(100% - 64px)' }"
      :collapse="isCollapse"
      @select="handleSelect"
    >
      <el-sub-menu index="1">
        <template #title>
          <el-icon><location /></el-icon>
          <span>Navigator One</span>
        </template>
        <el-menu-item-group>
          <template #title><span>Group One</span></template>
          <el-menu-item index="1-1">item one</el-menu-item>
          <el-menu-item index="1-2">item two</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="Group Two">
          <el-menu-item index="1-3">item three</el-menu-item>
        </el-menu-item-group>
        <el-sub-menu index="1-4">
          <template #title><span>item four</span></template>
          <el-menu-item index="1-4-1">item one</el-menu-item>
        </el-sub-menu>
      </el-sub-menu>
      <el-menu-item index="2">
        <el-icon><icon-menu /></el-icon>
        <template #title>Navigator Two</template>
      </el-menu-item>
      <el-menu-item index="3" disabled>
        <el-icon><document /></el-icon>
        <template #title>Navigator Three</template>
      </el-menu-item>
      <el-menu-item index="4" class="setting-item">
        <el-icon><setting /></el-icon>
        <template #title>设置</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<style scoped lang="scss">
.aside-main {
  @apply overflow-auto no-scrollbar h-full;
  background-color: var(--el-bg-color);

  .aside-header {
    border-right: solid 1px var(--el-border-color);
    .logo-wrapper {
      transition: width var(--el-transition-duration);
      .logo {
        @apply relative;
      }
    }
  }

  // 菜单调整宽度
  :deep(.el-sub-menu__title, .el-menu-item) {
    @apply pr-12;
  }

  &.aside-main--collapse {
    .aside-header {
      & > div {
        white-space: nowrap;
        width: calc(var(--el-menu-icon-width) + var(--el-menu-base-level-padding) * 2 - 1px);
      }
    }
  }
}
</style>
