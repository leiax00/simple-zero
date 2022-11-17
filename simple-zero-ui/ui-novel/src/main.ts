import { createApp } from 'vue'
import '@/styles/index.scss'
import ElementPlus from 'element-plus'
import renderWithQiankun, { qiankunWindow } from 'vite-plugin-qiankun/es/helper'
import App from './App.vue'
import type { QiankunProps } from 'vite-plugin-qiankun/es/helper'
import router from '@/router'
import pinia from '@/store'
import ripple from '@/components/directives/Ripple/ripple'

let serve: any = null
const render = (props: QiankunProps = {}) => {
  const { container } = props
  const app: string | Element =
    container?.querySelector('#novel-ui') || '#novel-ui' // 避免 id 重复导致微应用挂载失败
  serve = createApp(App)
  serve
    .directive('ripple', ripple)
    .use(pinia)
    .use(router)
    .use(ElementPlus)
    .mount(app)
}

const initQianKun = () => {
  renderWithQiankun({
    bootstrap() {
      console.log('微应用：bootstrap')
    },
    mount(props) {
      // 获取主应用传入数据
      console.log('微应用：mount', props)
      render(props)
    },
    unmount(props) {
      console.log('微应用：unmount', props)
      serve.unmount()
    },
    update(props) {
      console.log('微应用：update', props)
    },
  })
}

qiankunWindow.__POWERED_BY_QIANKUN__ ? initQianKun() : render() // 判断是否使用 qiankun ，保证项目可以独立运行
