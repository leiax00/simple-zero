<script setup lang="ts">
import { useServe } from '@/store/serve'

defineOptions({ name: 'Avatar' })

const serveStore = useServe()
const router = useRouter()
const routeTo = (path) => {
  router.push({ path })
}

const handleCommand = (command: string | number | object) => {
  switch (command) {
    case 'info':
      routeTo('/user')
      break
    case 'logout':
      serveStore.logoutWeb()
      break
    default:
    // do nothing
  }
}
</script>

<template>
  <div class="main-avatar inline-block">
    <el-dropdown v-if="serveStore.isLogin" popper-class="no-arrow" trigger="click" @command="handleCommand">
      <sz-icon icon-class="user" class="cursor-pointer icon-6 text-teal-500" />
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="info">
            <sz-icon icon-class="user-info" class="mb-2" />
            <div class="inline-block leading-6 pl-2">个人资料</div>
          </el-dropdown-item>
          <el-dropdown-item command="logout" divided>
            <sz-icon icon-class="logout" class="mb-2 text-red-500" />
            <div class="inline-block leading-6 pl-2 text-red-500">退出</div>
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <sz-icon v-else icon-class="user" class="cursor-pointer icon-6" @click="routeTo('/login')" />
  </div>
</template>

<style scoped lang="scss"></style>
