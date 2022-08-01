import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import pinia from '@/store'
import ElementPlus from 'element-plus'
import '@/styles/element/index.scss'
import ripple from '@/bean/directives/Ripple/ripple'
import { useApp } from '@/store/app'
import { startMicroApp4Main } from '@/utils/microApp'

const app = createApp(App)
app.directive('ripple', ripple)
app.use(router)
  .use(pinia)
  .use(ElementPlus)
  .mount('#app')

const appConf = useApp()
appConf.setApp(app)
startMicroApp4Main()
