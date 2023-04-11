import { createApp } from 'vue'
import '@/styles/index.scss'
import renderWithQiankun, { qiankunWindow } from 'vite-plugin-qiankun/es/helper'
import App from './App.vue'
import type { QiankunProps } from 'vite-plugin-qiankun/es/helper'
import router from '@/router'
import pinia from '@/store'

let serve: any = null
const render = (props: QiankunProps = {}) => {
  const { container } = props
  const app: string | Element =
    container?.querySelector('#app-tools') || '#app-tools' // 避免 id 重复导致微应用挂载失败
  serve = createApp(App)
  serve.use(pinia).use(router).mount(app)
}

const initQianKun = () => {
  renderWithQiankun({
    bootstrap() {
      // console.log('微应用：bootstrap')
    },
    mount(props) {
      // 获取主应用传入数据
      // console.log('微应用：mount', props)
      render(props)
    },
    unmount(props) {
      // console.log('微应用：unmount', props)
      serve.unmount()
    },
    update(props) {
      // console.log('微应用：update', props)
    },
  })
}

// 判断是否使用 qiankun ，保证项目可以独立运行
qiankunWindow.__POWERED_BY_QIANKUN__ ? initQianKun() : render()
