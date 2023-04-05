<template>
  <component :is="linkType" v-bind="dispachLink(to)" :class="clazz">
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { isEmptyStr } from '@leiax00/utils'
import { LINK_TYPE, linkProps } from './vars'
import type { LinkProps } from './vars'

defineOptions({ name: 'SzLink' })
const props = defineProps(linkProps)

const { to, type } = toRefs<LinkProps>(props)

const isExternal = computed(() => {
  return /^(https?:|mailto:|tel:)/.test(to.value)
})

const linkType = computed(() => {
  if (isExternal.value) {
    return 'a'
  }
  switch (type.value) {
    case LINK_TYPE.LINK:
    case LINK_TYPE.ROUTE_2_LINK:
      return 'a'
    default:
      return 'router-link'
  }
})

const clazz = computed(() => {
  switch (type.value) {
    case LINK_TYPE.LINK:
      return 'sz-link link'
    case LINK_TYPE.ROUTE:
      return 'sz-link route'
    case LINK_TYPE.ROUTE_2_LINK:
      return 'sz-link route-2-link'
    default:
      return 'sz-link link-2-route'
  }
})

const dispachLink = function (path) {
  if (isEmptyStr(path)) {
    return {}
  }
  if (isExternal.value) {
    return {
      href: path,
      target: '_blank',
      rel: 'noopener',
    }
  }
  return {
    to: path,
  }
}
</script>

<style lang="scss" scoped>
.sz-link {
  &.link {
  }
  &.route {
  }
  &.route-2-link {
  }
  &.link-2-route {
  }
}
</style>
