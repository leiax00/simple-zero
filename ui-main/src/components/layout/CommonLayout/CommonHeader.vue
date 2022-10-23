<template>
  <el-row class="common-header">
    <el-col :span="24" class="header-nav">
      <div :class="clazz">
        <div class="nav-item header-logo">
          <a class="nav-item" href="/"><img :src="logoUrl" alt="Simple Zero" class="h-8"></a>
        </div>
        <div class="nav-item header-link">
          <div v-for="(item, index) in headers" :key="index" class="route-item inline-block">
            <router-link :to="item.path" class="font-bold">
              {{ item.name }}
            </router-link>
          </div>
        </div>
        <div class="nav-item header-right-nav">right nav</div>
      </div>
    </el-col>
    <el-col v-if="showTitle" :span="24" class="header-title">
      <common-title />
      <wave />
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { useApp } from '@/store/app'
import Wave from '@/components/basic/animations/Wave.vue'
import CommonTitle from '@/components/layout/CommonLayout/CommonTitle/CommonTitle.vue'
import { computed, onBeforeUnmount, reactive, ref } from 'vue'

defineOptions({ name: 'CommonHeader' })
const appConf = useApp()
const logoUrl = appConf.logoUrl
const headers = appConf.config.headers
const navState = reactive({ scrollTop: 0, preScrollTop: 0 })
const clazz = computed(() => {
  return {
    'main-nav': true,
    // 往下滚动时, 自动隐藏nav
    'fixed-top': navState.scrollTop !== 0 && navState.scrollTop > navState.preScrollTop,
    // 往上滚动时添加背景色, 因为可能和正文重叠
    'with-bg': navState.scrollTop !== 0 && navState.scrollTop < navState.preScrollTop
  }
})

const showTitle = computed(() => {
  // const route = useRoute()
  return false
})

const titleBg = ref(`url(${appConf.getPicUrl('bg-load.png')})`)

const handleScroll = function () {
  navState.preScrollTop = navState.scrollTop
  navState.scrollTop = document.documentElement.scrollTop || document.body.scrollTop
}
document.addEventListener('scroll', handleScroll)
onBeforeUnmount(() => {
  document.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
.common-header {
  .header-nav {
    a {
      @apply leading-8;
    }

    .main-nav {
      @apply px-6 h-16 w-full;
      // 1.5rem == 24px
      @apply flex;
      @apply top-0 left-0 fixed z-10;
      &.with-bg {
        @apply bg-neutral-700 opacity-80  ;
      }

      &.fixed-top {
        @apply -top-16;
        // 隐藏nav, 设置为nav高度
      }

      .nav-item {
        @apply py-4;
      }

      .header-logo {
        @apply max-w-logo flex-logo;
      }

      .header-link {
        &.nav-item {
          @apply py-0;
        }

        @apply flex-grow px-6;
        .route-item {
          @apply text-teal-500 px-4 py-4 cursor-pointer;
          &:hover {
            //@apply bg-neutral-600 opacity-50;
          }
        }
      }

      .header-right-nav {
        @apply max-w-px-200 flex-px-200
      }
    }
  }

  .header-title {
    background: v-bind(titleBg) no-repeat scroll center center;
    background-size: cover;
  }

}
</style>
