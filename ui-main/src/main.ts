import { createApp } from 'vue'
import App from './App.vue'
import pinia from '@/store'
import router, { updateRouterByServes } from '@/router'
import ElementPlus from 'element-plus'
// import '@/styles/element/index.scss'
import '@/styles/index.scss'
import ripple from '@/bean/directives/Ripple/ripple'
import { loadAppConf } from '@/config'
import { useApp } from '@/store/app'
// import { useApp } from '@/store/app'
// import { registerMicroApps, start } from 'qiankun'

loadAppConf().then((conf: any) => {
  updateRouterByServes(conf.serves || [])
  const app = createApp(App)
  app.directive('ripple', ripple)
  app.use(pinia)
    .use(router)
    .use(ElementPlus)
    .mount('#app')

  const appConf = useApp()
  appConf.setConfig(conf)
})

// startQianQun()

// function startQianQun() {
//   const appConf = useApp()
//   const qianQunServeList = []
//   appConf.fetchAppList().forEach(item => {
//     qianQunServeList.push({
//       name: item.name,
//       entry: item.domain,
//       container: `#${item.name}`, // 和app.vue配置的节点
//       activeRule: item.prefix,
//       props: {}
//     })
//   })
//   registerMicroApps(qianQunServeList)
//   start()
// }
