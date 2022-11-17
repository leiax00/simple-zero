<template>
  <div class="wave-main">
    <svg
      class="preview-waves"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      viewBox="0 24 150 28"
      preserveAspectRatio="none"
      shape-rendering="auto"
    >
      <defs>
        <path
          id="gentle-wave"
          d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z"
        />
      </defs>
      <g class="preview-parallax">
        <use xlink:href="#gentle-wave" x="48" y="0" :fill="getColor(0)" />
        <use xlink:href="#gentle-wave" x="48" y="3" :fill="getColor(1)" />
        <use xlink:href="#gentle-wave" x="48" y="5" :fill="getColor(2)" />
        <use xlink:href="#gentle-wave" x="48" y="7" :fill="getColor(3)" />
      </g>
    </svg>
  </div>
</template>

<script>
import colors from 'tailwindcss/colors'
import { getRgbNumList } from '@/utils/colorUtils'

export default {
  name: 'Wave',
  computed: {
    color() {
      return getRgbNumList(colors.neutral['800'])
    },
  },
  methods: {
    getColor(id) {
      const multiplier = [0.7, 0.5, 0.3, 1]
      return `rgba(${this.color.join(', ')}, ${multiplier[id]})`
    },
  },
}
</script>

<style lang="scss" scoped>
// 浪花特效
@keyframes v-wave-forever {
  0% {
    transform: translate3d(-90px, 0, 0);
  }
  100% {
    transform: translate3d(85px, 0, 0);
  }
}

.wave-main {
  width: 100%;
  position: relative;
  left: 0;
  right: 0;
  z-index: 2;
  .preview-waves {
    position: relative;
    width: 100%;
    height: 0vh;
    margin-bottom: -8px;
    min-height: 100px;
    max-height: 150px;
    .preview-parallax > use {
      animation: v-wave-forever 25s cubic-bezier(0.55, 0.5, 0.45, 0.5) infinite;
      &:nth-child(1) {
        animation-delay: -2s;
        animation-duration: 7s;
      }
      &:nth-child(2) {
        animation-delay: -3s;
        animation-duration: 10s;
      }
      &:nth-child(3) {
        animation-delay: -4s;
        animation-duration: 13s;
      }
      &:nth-child(4) {
        animation-delay: -5s;
        animation-duration: 20s;
      }
    }
  }
}
</style>
