import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { getToken, tipMsg } from '../compositive'
import type { R } from './domain'

const service = axios.create({
  timeout: 5 * 1000,
})

service.interceptors.request.use(
  (config) => {
    // 是否需要设置 token
    const needToken = (config.headers || {}).needToken !== false
    // 是否需要防止数据重复提交
    const preventRepeat = (config.headers || {}).preventRepeat !== false
    const token = getToken()
    if (token && !needToken) {
      config.headers['Authorization'] = `Bearer ${token}` // 增加前缀Bearer
    }
    const time = Date.now()
    const reqCache = useStorage('req-cache', { url: '', time: 0 })
    if (preventRepeat && config.url === reqCache.value.url && time - reqCache.value.time < 1000) {
      return Promise.reject(new Error('重复的数据提交'))
    }
    reqCache.value.url = config.url || ''
    reqCache.value.time = time

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
