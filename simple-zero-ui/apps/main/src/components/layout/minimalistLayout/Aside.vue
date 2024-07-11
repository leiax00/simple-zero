<script setup lang="tsx">
import { onClickOutside, useMagicKeys, useWindowSize } from '@vueuse/core'
import { breakpointsTailwind } from '@leiax00/constants'
import { isExternalUrl } from '@leiax00/utils'
import { Location, Setting } from '@element-plus/icons-vue'
import { useApp } from '@/store/app'

defineOptions({ name: 'MinimalistAside' })
const { logoUrl, sortedMenus } = useApp()

const isCollapse = ref(true)
const showTextLogo = ref(true)
// aside是否脱离文档流, 最大程度保证页面布局不变动(仅收起状态的侧边栏占位)
const asideFloat = ref(true)

const routeMap = computed(() => {
  const rst: Record<string, string> = {}
  for (const menu of sortedMenus) {
    for (const menuItem of menu.data) {
      rst[`${menu.id}-${menuItem.id}`] = menuItem.path
    }
  }
  return rst
})

const router = useRouter()

const handleSelect = (index: string, indexPath: string[]) => {
  const path = routeMap.value[indexPath.join('-')]
  if (isExternalUrl(path)) {
    window.open(path, '_blank')
  } else {
    router.push(path)
  }
  isCollapse.value = true
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

  if (isCollapse.value) {
    showTextLogo.value = true
  } else {
    setTimeout(() => {
      showTextLogo.value = false
    }, 300)
  }
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
const headerH = '40px'
</script>

<template>
  <div ref="aside" :class="{ 'aside-main': true, ...asideClazz }">
    <div class="aside-header" @click="() => (isCollapse = !isCollapse)">
      <div
        class="logo-wrapper flex flex-row items-center pl-3"
        title="显示/隐藏侧边栏Ctrl+`"
        :style="{ height: headerH }"
      >
        <span class="logo contents">
          <img v-if="showTextLogo" src="https://static.leiax00.cn/dev/pics/logo-sz.png" alt="Simple Zero" class="w-5" />
          <img v-else :src="logoUrl" alt="Simple Zero" class="w-32" />
        </span>
      </div>
    </div>
    <el-menu
      default-active="2"
      :collapse-transition="true"
      :style="{ 'min-height': `calc(100% - ${headerH})` }"
      :collapse="isCollapse"
      @select="handleSelect"
    >
      <template v-for="menu in sortedMenus">
        <el-menu-item
          v-if="menu.data.length === 1"
          :key="`${menu.id}-${menu.data[0].id}`"
          :index="`${menu.id}-${menu.data[0].id}`"
        >
          <!-- todo icon: menu.data[0].icon -->
          <el-icon><location /></el-icon>
          <template #title>{{ menu.data[0].name }}</template>
        </el-menu-item>
        <el-sub-menu v-if="menu.data.length > 1" :key="`${menu.id}`" :index="menu.id">
          <template #title>
            <!-- todo icon: menu.icon -->
            <el-icon><location /></el-icon>
            <span>{{ menu.name }}</span>
          </template>
          <el-menu-item v-for="menuItem in menu.data" :key="menuItem.id" :index="menuItem.id">
            <!-- todo icon: menu.data[0].icon -->
            <el-icon><location /></el-icon>
            <template #title>{{ menuItem.name }}</template>
          </el-menu-item>
        </el-sub-menu>
      </template>
      <el-menu-item index="app-settings" class="setting-item">
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
  :deep(.el-menu) {
    .el-sub-menu__title {
      @apply pr-32;
    }

    &.el-menu--collapse {
      .el-sub-menu__title {
        padding: 0 var(--el-menu-base-level-padding);
      }
    }
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
