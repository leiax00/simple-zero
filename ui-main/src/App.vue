<script setup lang="ts">
import { onMounted } from 'vue'

// async function loadAppConf() {
//   const { Base64, Utf8 } = CryptoJS.enc
//   const { data } = await axios.post('https://etcd.leiax00.cn/v3/auth/authenticate', {
//     name: 'root',
//     password: 'lax4832.'
//   })
//   const headers = { Authorization: data.token }
//   // await axios.post('https://etcd.leiax00.cn/v3/kv/put', {
//   //   key: Base64.stringify(Utf8.parse('app.ui.ui-main')),
//   //   value: Base64.stringify(Utf8.parse(JSON.stringify(settings)))
//   // }, { headers })
//   // 查询以 app.ui开头的所有服务的配置
//   const resp = await axios.post('https://etcd.leiax00.cn/v3/kv/range', {
//     key: Base64.stringify(Utf8.parse('app.ui.ui-main'))
//     // range_end: Base64.stringify(Utf8.parse('app.ui' + 1))
//   }, { headers })
//   let conf = {}
//   if (resp.data.kvs) {
//     const confStr = Utf8.stringify(Base64.parse(resp.data.kvs[0].value))
//     conf = JSON.parse(confStr)
//   }
//   return Promise.resolve(conf)
// }
//
// function loadDynamicRoutes(router: Router, conf: any) {
//   if (!conf.serves || conf.serves.length <= 0) {
//     return
//   }
//   conf.serves.forEach((item: any) => {
//     router.addRoute({
//       path: item.prefix,
//       name: item.name,
//       component: () => import('@/views/appList/AppList.vue'),
//       meta: {
//         title: item.name,
//         roles: [],
//         serve: item
//       }
//     })
//   })
// }

onMounted(async () => {
  // const appConf = useApp()
  // const router = useRouter()
  // const conf = await loadAppConf()
  // appConf.setConfig(conf)
  // loadDynamicRoutes(router, conf)
})
</script>

<template>
  <router-view />
</template>

<style lang="scss">
</style>
