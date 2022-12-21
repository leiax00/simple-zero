import '@/styles/preflight.css'
import { createApp } from 'vue'
import App from './App.vue'
import '@/styles/index.scss'
import { loadAppConf } from './config'
import pinia from '@/store'
import router, { updateRouterByServes } from '@/router'
import { useApp } from '@/store/app'
loadAppConf().then((conf: any) => {
  updateRouterByServes(conf.serves || [])
  const app = createApp(App)
  app.use(pinia).use(router).mount('#app')
  const appConf = useApp()
  appConf.setConfig(conf)
})
