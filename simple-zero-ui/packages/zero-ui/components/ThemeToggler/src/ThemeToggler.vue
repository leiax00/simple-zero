<template>
  <div class="theme-toggler" @click="() => toggleDark()">
    <div class="switch__action">
      <div class="switch__icon">
        <el-icon :size="13">
          <svg class="dark-icon" viewBox="0 0 24 24">
            <path
              d="M11.01 3.05C6.51 3.54 3 7.36 3 12a9 9 0 0 0 9 9c4.63 0 8.45-3.5 8.95-8c.09-.79-.78-1.42-1.54-.95A5.403 5.403 0 0 1 11.1 7.5c0-1.06.31-2.06.84-2.89c.45-.67-.04-1.63-.93-1.56z"
              fill="currentColor"
            />
          </svg>
          <svg class="light-icon" viewBox="0 0 24 24">
            <path
              d="M6.05 4.14l-.39-.39a.993.993 0 0 0-1.4 0l-.01.01a.984.984 0 0 0 0 1.4l.39.39c.39.39 1.01.39 1.4 0l.01-.01a.984.984 0 0 0 0-1.4zM3.01 10.5H1.99c-.55 0-.99.44-.99.99v.01c0 .55.44.99.99.99H3c.56.01 1-.43 1-.98v-.01c0-.56-.44-1-.99-1zm9-9.95H12c-.56 0-1 .44-1 .99v.96c0 .55.44.99.99.99H12c.56.01 1-.43 1-.98v-.97c0-.55-.44-.99-.99-.99zm7.74 3.21c-.39-.39-1.02-.39-1.41-.01l-.39.39a.984.984 0 0 0 0 1.4l.01.01c.39.39 1.02.39 1.4 0l.39-.39a.984.984 0 0 0 0-1.4zm-1.81 15.1l.39.39a.996.996 0 1 0 1.41-1.41l-.39-.39a.993.993 0 0 0-1.4 0c-.4.4-.4 1.02-.01 1.41zM20 11.49v.01c0 .55.44.99.99.99H22c.55 0 .99-.44.99-.99v-.01c0-.55-.44-.99-.99-.99h-1.01c-.55 0-.99.44-.99.99zM12 5.5c-3.31 0-6 2.69-6 6s2.69 6 6 6s6-2.69 6-6s-2.69-6-6-6zm-.01 16.95H12c.55 0 .99-.44.99-.99v-.96c0-.55-.44-.99-.99-.99h-.01c-.55 0-.99.44-.99.99v.96c0 .55.44.99.99.99zm-7.74-3.21c.39.39 1.02.39 1.41 0l.39-.39a.993.993 0 0 0 0-1.4l-.01-.01a.996.996 0 0 0-1.41 0l-.39.39c-.38.4-.38 1.02.01 1.41z"
              fill="currentColor"
            />
          </svg>
        </el-icon>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core'

defineOptions({ name: 'ThemeToggler' })
const isDark = useDark({
  storageKey: 'theme-appearance',
})

const toggleDark = useToggle(isDark)
</script>

<style lang="scss" scoped>
.theme-toggler {
  margin: 0;
  display: inline-block;
  position: relative;
  width: 40px;
  height: 20px;
  border: 1px solid var(--el-border-color);
  outline: none;
  border-radius: 10px;
  box-sizing: border-box;
  background: var(--sz-bg-color-mute);
  cursor: pointer;
  transition: border-color var(--el-transition-duration), background-color var(--el-transition-duration);

  .switch__action,
  .switch__icon {
    width: 16px;
    height: 16px;
  }

  .switch__action {
    position: absolute;
    top: 1px;
    left: 1px;
    border-radius: 50%;
    background-color: var(--el-bg-color);
    transform: translateX(0);
    color: var(--text-color-light);
    transition: border-color var(--el-transition-duration), background-color var(--el-transition-duration),
      transform var(--el-transition-duration);

    .switch__icon {
      @apply relative;
      .el-icon {
        @apply cursor-pointer;
        position: absolute;
        left: 1px;
        bottom: 1px;

        .el-icon svg {
          height: 1em;
          width: 1em;
        }

        .dark-icon,
        .light-icon {
          transition: color var(--el-transition-duration), opacity var(--el-transition-duration);
        }

        .light-icon {
          opacity: 1;
          position: absolute;
          top: 0;
          left: 0;
        }

        .dark-icon {
          opacity: 0;
          position: absolute;
          top: 0;
          left: 0;
        }
      }
    }
  }
}

.dark {
  .theme-toggler {
    .switch__action {
      transform: translateX(20px);
      .switch__icon {
        .el-icon {
          .dark-icon {
            opacity: 1;
          }

          .light-icon {
            opacity: 0;
          }
        }
      }
    }
  }
}
</style>
