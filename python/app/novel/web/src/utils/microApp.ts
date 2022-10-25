import microApp from '@micro-zoe/micro-app'
import { useApp } from '@/store/app'
import { Router } from 'vue-router'
import router from '@/router'

export function startMicroApp4Main() {
  const appConf = useApp()
  const appList = appConf.fetchAppList()
  const modules: any = {}
  appList.forEach(function (item: {name: string, prefix: string, domain: string}) {
    modules[item.name] = [
      {
        loader (code: any) {
          if (process.env.NODE_ENV === 'development') {
            // 这里 /basename/ 需要和子应用vite.config.js中base的配置保持一致
            const reg = new RegExp(`(from|import)(\\s*['"])(${item.prefix})`, 'g')
            code = code.replace(reg, (all: string) => {
              return all.replace(item.prefix, `${item.domain}${item.prefix}`)
            })
          }
          return code
        }
      }
    ]
  })

  microApp.start({
    plugins: {
      modules
    }
  })
}

export function startMicroApp4Child () {
  const appConf = useApp()
  const eventCenterForApp = (window as any).eventCenterForApp
  handleMicroData(router)

  window.addEventListener('unmount', function () {
    appConf.app?.unmount()
    eventCenterForApp?.clearDataListener()
    console.log('微应用child-vite卸载了')
  })

  // 与基座进行数据交互
  function handleMicroData (router: Router) {
    // eventCenterForApp 是基座添加到window的数据通信对象
    if (eventCenterForApp) {
      // 主动获取基座下发的数据
      console.log('child-vite getData:', eventCenterForApp.getData())

      // 监听基座下发的数据变化
      eventCenterForApp.addDataListener((data: Record<string, unknown>) => {
        console.log('child-vite addDataListener:', data)

        if (data.path && typeof data.path === 'string') {
          data.path = data.path.replace(/^#/, '')
          // 当基座下发path时进行跳转
          if (data.path && data.path !== router.currentRoute.value.path) {
            router.push(data.path as string)
          }
        }
      })

      // 向基座发送数据
      setTimeout(() => {
        eventCenterForApp.dispatch({ myname: 'novel-ui' })
      }, 3000)
    } else {
      router.push({ path: '/' })
    }
  }
}
