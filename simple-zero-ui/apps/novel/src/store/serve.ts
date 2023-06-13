import { defineStore } from 'pinia'

export const useServe = defineStore('serveData', {
  state: () => ({
    j2wx: {
      channelList: [
        { name: '古代言情', channelKey: 'gywx', color: '', bgColor: '' },
        { name: '都市青春', channelKey: 'dsyq', color: '', bgColor: '' },
        { name: '幻想现言', channelKey: 'qqyq', color: '', bgColor: '' },
        { name: '古代穿越', channelKey: 'gdcy', color: '', bgColor: '' },
        { name: '奇幻言情', channelKey: 'xhqh', color: '', bgColor: '' },
        { name: '未来游戏悬疑', channelKey: 'xywy', color: '', bgColor: '' },
        { name: '都市现纯', channelKey: 'xddm', color: '', bgColor: '' },
        { name: '幻想现纯', channelKey: 'blhx', color: '', bgColor: '' },
        { name: '古代纯爱', channelKey: 'gddm', color: '', bgColor: '' },
        { name: '百合小说', channelKey: 'bhxs', color: '', bgColor: '' },
        { name: '无CP', channelKey: 'nocp', color: '', bgColor: '' },
      ],
    },
  }),
  getters: {
    getChannel: (state) => {
      return (channelKey: string): any => state.j2wx.channelList.find((item) => item.channelKey === channelKey)
    },
  },
  actions: {},
})
