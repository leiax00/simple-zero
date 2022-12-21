import type { ExtractPropTypes } from 'vue'
import type Icon from './SzIcon.vue'

export const iconProps = {
  iconClass: {
    type: String,
    required: true,
  },
  className: {
    type: String,
    default: '',
  },
}
export type IconProps = ExtractPropTypes<typeof iconProps>
export type IconInstance = InstanceType<typeof Icon>
