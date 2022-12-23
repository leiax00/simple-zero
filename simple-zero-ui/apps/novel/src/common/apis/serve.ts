import axios from 'axios'

const getBaseUrl = () => {
  const domain = import.meta.env.VITE_APP_DOMAIN.endsWith('/')
    ? import.meta.env.VITE_APP_DOMAIN.slice(
        0,
        import.meta.env.VITE_APP_DOMAIN.length - 1
      )
    : import.meta.env.VITE_APP_DOMAIN
  const prefix = import.meta.env.VITE_APP_PREFIX.startsWith('/')
    ? import.meta.env.VITE_APP_PREFIX.slice(1)
    : import.meta.env.VITE_APP_PREFIX
  return `${domain}/${prefix}`
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
    return Promise.reject(error)
  }
)

export default serve
