import { ElMessage } from 'element-plus'

export const tipMsg = (message: string, type: any, showClose = true) => {
  if (!['success', 'warning', 'error'].includes(type)) {
    type = undefined
  }
  ElMessage({ showClose, message, type })
}
