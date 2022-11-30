import { createApp } from 'vue'
import App from './App.vue'
import pinia from '@/store'
import router, { updateRouterByServes } from '@/router'
import '@/styles/index.scss'
import { loadAppConf } from '@/config'
import { useApp } from '@/store/app'

loadAppConf().then((conf: any) => {
  updateRouterByServes(conf.serves || [])
  const app = createApp(App)
  app
    .use(pinia)
    .use(router)
    // .use(ZeroUi)
    .mount('#app')

  const appConf = useApp()
  appConf.setConfig(conf)
})
