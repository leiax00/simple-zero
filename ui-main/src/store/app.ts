import { defineStore } from 'pinia'
// @ts-ignore
import settings from '@/settings.yaml'
import { App } from 'vue'
import commonUtil from '@/utils/commonUtil'
import { useScriptTag } from '@vueuse/core'

export const useApp = defineStore('app', {
  state: (): {
    config: any,
    app?: App<Element>,
    uiCtl: any
  } => {
    return {
      config: settings,
      app: undefined,
      uiCtl: {
        showArticle: false,
        isLoaded4svgSrc: false
      }
    }
  },
  getters: {
    logoUrl: (state) => {
      const { base, opts } = state.config.app.picCdn
      if (commonUtil.isEmptyStr(opts.pic) || opts.pic.trim() === '/') {
        return `${base}/logo-simple_zero.png`
      }
      return `${base}/${opts.pic}/logo-simple_zero.png`
    }
  },
  actions: {
    setApp(app: App<Element>) {
      this.app = app
    },
    fetchAppList() {
      return this.config.services || []
    },
    async loadSvgSrc(cb?: Function) {
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
    getPicUrl(params: Object|string) {
      const { base, opts } = this.config.app.picCdn
      if (commonUtil.isEmptyStr(opts.pic) || opts.pic.trim() === '/') {
        return `${base}/${params}`
      }
      return `${base}/${opts.pic}/${params}`
    }
  }
})
