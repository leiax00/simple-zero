import { defineStore } from 'pinia'
import { useScriptTag } from '@vueuse/core'
import type { StoreDefinition } from 'pinia'
import type { App } from 'vue'
import type { EtcdConf, Menu } from '@/beans'

export const useApp: StoreDefinition = defineStore('app', {
  state: (): {
    config: EtcdConf
    app?: App<Element>
    uiCtl: any
  } => {
    return {
      config: { menus: [], serves: [] },
      app: undefined,
      uiCtl: {
        showAside: false,
        isLoaded4svgSrc: false,
      },
    }
  },
  getters: {
    picUri(): string {
      return `${this.config.common?.static}/pics`
    },
    logoUrl(): string {
      return `${this.picUri}/logo-simple_zero.png`
    },
    sortedMenus(): Menu[] {
      const tmpMenu = this.config.menus.map((item) => {
        const tmpItem = { ...item }
        tmpItem.data = item.data.sort((a, b) => {
          return (b.showWeight || 0) - (a.showWeight || 0)
        })
        return tmpItem as Menu
      })
      return tmpMenu.sort((a, b) => {
        return (b.showWeight || 0) - (a.showWeight || 0)
      })
    },
  },
  actions: {
    setApp(app: any) {
      this.app = app
    },
    fetchAppList() {
      return this.config.serves || []
    },
    setConfig(conf: EtcdConf) {
      this.config = conf
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      // this.loadSvgSrc().then(() => {})
    },
    async loadSvgSrc(cb?: () => void) {
      if (!this.uiCtl.isLoaded4svgSrc) {
        const { load } = useScriptTag(
          this.config.common?.svgUri || '',
          // on script tag loaded.
          () => {
            cb && cb()
          },
          { manual: true }
        )
        await load()
        this.uiCtl.isLoaded4svgSrc = true
      }
    },
  },
})
