import { useBreakpoints } from '@vueuse/core'

export const breakpointsTailwind = {
  sm: 640,
  md: 992,
  lg: 1280,
  xl: 1920,
}

export const breakpoints = useBreakpoints(breakpointsTailwind)
