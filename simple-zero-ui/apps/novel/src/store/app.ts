import { defineStore } from 'pinia'
import type { App } from 'vue'

export const useApp = defineStore('app', {
  state: (): {
    app?: App<Element>
  } => {
    return {
      app: undefined,
    }
  },
  getters: {},
  actions: {
    setApp(app: App<Element>) {
      this.app = app
    },
  },
})