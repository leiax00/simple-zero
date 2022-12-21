import { defineStore } from 'pinia'
import { useScriptTag } from '@vueuse/core'
import { isEmptyStr } from '@leiax00/utils'
import type { App } from 'vue'

export const useApp = defineStore('app', {
  state: (): {
    config: any
    app?: App<Element>
    uiCtl: any
  } => {
    return {
      config: {},
      app: undefined,
      uiCtl: {
        showArticle: false,
        isLoaded4svgSrc: false,
      },
    }
  },
  getters: {
    logoUrl: (state) => {
      const { base, opts } = state.config.app.picCdn
      if (isEmptyStr(opts.pic) || opts.pic.trim() === '/') {
        return `${base}/logo-simple_zero.png`
      }
      return `${base}/${opts.pic}/logo-simple_zero.png`
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
          this.config.app.srcSvg,
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
      return `${base}/${opts.pic}/${params}`
    },
  },
})
