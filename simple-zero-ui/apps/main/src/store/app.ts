import { defineStore } from 'pinia'
import { useScriptTag } from '@vueuse/core'
import { isEmptyStr } from '@leiax00/utils'
import type { StoreDefinition } from 'pinia'
import type { App } from 'vue'

export const useApp: StoreDefinition = defineStore('app', {
  state: (): {
    config: any
    app?: App<Element>
    uiCtl: any
  } => {
    return {
      config: {},
      app: undefined,
      uiCtl: {
        showAside: false,
        isLoaded4svgSrc: false,
      },
    }
  },
  getters: {
    picUri(): string {
      return `${this.config.common.static}/pics`
    },
    logoUrl(): string {
      return `${this.picUri}/logo-simple_zero.png`
    },
  },
  actions: {
    setApp(app: any) {
      this.app = app
    },
    fetchAppList() {
      return this.config.serves || []
    },
    setConfig(conf: any) {
      this.config = conf
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      this.loadSvgSrc().then(() => {})
    },
    async loadSvgSrc(cb?: () => void) {
      if (!this.uiCtl.isLoaded4svgSrc) {
        const { load } = useScriptTag(
          this.config.common.svgUri,
          // on script tag loaded.
          (el: HTMLScriptElement) => {
            cb && cb()
          },
          { manual: true }
        )
        await load()
        this.uiCtl.isLoaded4svgSrc = true
      }
    },
    getPicUrl(params: any) {
      const { base, opts } = this.config.app.picCdn
      if (isEmptyStr(opts.pic) || opts.pic.trim() === '/') {
        return `${base}/${params}`
      }
      return `${this.picUri}/${params}`
    },
  },
})
