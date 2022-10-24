import axios from 'axios'

const serve = axios.create({
  baseURL: `${import.meta.env.VITE_APP_DOMAIN}${import.meta.env.VITE_APP_PREFIX}`,
  timeout: 10 * 1000,
  headers: {}
})

serve.interceptors.request.use(
  config => {
    return config
  }, error => {
    return Promise.reject(error)
  }
)

serve.interceptors.response.use(
  resp => {
    return Promise.resolve(resp.data)
  }, error => {
    return Promise.reject(error)
  }
)

export default serve
