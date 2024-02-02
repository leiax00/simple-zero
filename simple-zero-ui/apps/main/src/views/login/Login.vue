<script setup lang="ts">
import { useServe } from '@/store/serve'

defineOptions({ name: 'PageLogin' })

const formData = reactive({ username: '', password: '' })

const serve = useServe()
const router = useRouter()
const onSubmit = () => {
  serve.loginWeb(formData).then(() => {
    router.push('/')
  })
}
</script>

<template>
  <div class="main-login w-full h-full flex flex-col justify-center items-center">
    <el-card class="p-6">
      <el-form :model="formData" label-width="auto">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="formData.password" type="password" show-password />
        </el-form-item>
        <div class="flex flex-row justify-center pt-6">
          <el-button type="primary" class="w-full" @click="onSubmit">登录</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<style lang="scss"></style>
