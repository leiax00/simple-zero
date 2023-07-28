import axios from 'axios'
import { tipMsg } from '@leiax00/zero-ui'

const getBaseUrl = () => {
  return `/api/${import.meta.env.VITE_APP_NAME}/${import.meta.env.VITE_APP_VERSION}`
}

const serve = axios.create({
  baseURL: getBaseUrl(),
  timeout: 10 * 1000,
  headers: {},
})

serve.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

serve.interceptors.response.use(
  (resp) => {
    return Promise.resolve(resp.data)
  },
  (error) => {
    tipMsg('网络异常,请稍后重试!', 'error')
    return Promise.reject(error)
  }
)

export default serve
