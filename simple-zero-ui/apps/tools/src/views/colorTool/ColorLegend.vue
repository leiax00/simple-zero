<template>
  <div class="color-legend">
    <div class="title-level-2">取色板</div>
    <div class="content-wrapper">
      <template v-for="(val, key) in colors">
        <template v-if="typeof val === 'object'">
          <div v-for="(color, no) in val" :key="`${key}-${no}`" class="color-wrapper" @click="copy({ key, no, color })">
            <div class="color-item">
              <div class="color-picker__color" :style="{ backgroundColor: color }" />
              <div class="color-picker__name">{{ key }}-{{ no }}</div>
              <div class="color-picker__value">{{ color }}</div>
            </div>
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import colors from 'tailwindcss/colors'
import useClipboard from 'vue-clipboard3'
import { ElMessage } from 'element-plus'

defineOptions({ name: 'ColorLegend' })
const props = defineProps({
  pickColor: {
    type: String,
    required: true,
  },
})

const { pickColor } = toRefs(props)

const { toClipboard } = useClipboard()

const copyColor = ref(true)
const copy = async (colorObj: { key: string; no: string; color: string }) => {
  try {
    const content = copyColor.value ? colorObj.color : `${colorObj.key}-${colorObj.no}`
    await toClipboard(content)
    pickColor.value = colorObj.color
    ElMessage({
      showClose: true,
      message: `color: ${colorObj.color} copied!`,
      type: 'success',
    })
  } catch (e) {
    console.error(e)
    ElMessage({
      showClose: true,
      message: `color: ${colorObj.color} copy failed!`,
      type: 'error',
    })
  }
}
</script>

<style scoped lang="scss">
.color-legend {
  .content-wrapper {
    @apply flex flex-wrap gap-4;
    .color-wrapper {
      @apply flex-grow flex justify-center items-center;
      @apply cursor-pointer;
      .color-item {
        .color-picker__color {
          @apply rounded h-10;
          width: 100px;
        }

        .color-picker__name {
          @apply text-xs;
        }

        .color-picker__value {
          @apply text-xs;
        }
      }
    }
  }
}
</style>
