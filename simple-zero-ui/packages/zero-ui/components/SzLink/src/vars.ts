import type { ExtractPropTypes } from 'vue'
import type SzLink from './SzLink.vue'

export const LINK_TYPE = {
  ROUTE: 'route',
  LINK: 'link',
  ROUTE_2_LINK: 'route_2_link',
  LINK_2_ROUTE: 'link_2_route',
}

export const linkProps = {
  type: {
    type: String,
    default: 'route',
  },
  to: {
    type: String,
    default: '',
  },
}

export type LinkProps = ExtractPropTypes<typeof linkProps>
export type LinkInstance = InstanceType<typeof SzLink>
