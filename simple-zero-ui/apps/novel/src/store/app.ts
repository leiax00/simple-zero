import { defineStore } from 'pinia'
import type { App } from 'vue'

export const useApp = defineStore('app', {
  state: (): {
    app?: App<Element>
    routeData: object
  } => {
    return {
      app: undefined,
      routeData: {},
    }
  },
  getters: {},
  actions: {
    setApp(app: App<Element>) {
      // @ts-ignore
      this.app = app
    },
    setRouteData(data: object) {
      this.routeData = data
    },
  },
})
