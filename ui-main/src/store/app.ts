import { defineStore } from 'pinia'
import settings from '@/settings'
import { App } from 'vue'

export const useApp = defineStore('app', {
  state: (): {
    config: any,
    app?: App<Element>
  } => {
    return {
      config: settings,
      app: undefined
    }
  },
  getters: {

  },
  actions: {
    setApp(app: App<Element>) {
      this.app = app
    },
    fetchAppList() {
      return this.config.services || []
    }
  }
})
