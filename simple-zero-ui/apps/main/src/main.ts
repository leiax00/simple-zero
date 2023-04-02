import '@/styles/preflight.css'
import { createApp } from 'vue'
import App from './App.vue'
import '@/styles/index.scss'
import pinia from '@/store'
import router, { updateRouterByServes } from '@/router'
import { useAppCtl } from '@/store/app'
import { loadAppConf } from '@/config'

const app = createApp(App)
app.use(pinia).use(router).mount('#app')
// loadAppConf().then((conf: any) => {
//   updateRouterByServes(conf.serves || [])
//
//   const appConf = useAppCtl()
//   appConf.setConfig(conf)
// })
