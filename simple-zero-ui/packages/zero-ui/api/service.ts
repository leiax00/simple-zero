import axios from 'axios'
import { tipMsg } from '../compositive'
import type { R } from './domain'

const service = axios.create({
  timeout: 5 * 1000,
})

service.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (resp) => {
    const serverData = resp.data as R<any>
    if (serverData.code === 200) {
      return Promise.resolve(serverData.data)
    } else {
      tipMsg(`${serverData.msg}`, 'error')
      return Promise.reject(serverData)
    }
  },
  (err) => {
    tipMsg('请求API失败, 请稍后重试!', 'error')
    return Promise.reject(err)
  }
)

export default service
