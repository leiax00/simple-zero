import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import pinia from '@/store'
import ElementPlus from 'element-plus'
// import '@/styles/element/index.scss'
import '@/styles/index.scss'
import ripple from '@/bean/directives/Ripple/ripple'
// import { useApp } from '@/store/app'
// import { registerMicroApps, start } from 'qiankun'

const app = createApp(App)
app.directive('ripple', ripple)
app.use(router)
  .use(pinia)
  .use(ElementPlus)
  .mount('#app')

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
