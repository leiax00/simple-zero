import CryptoJS from 'crypto-js'
import axios from 'axios'

export async function loadAppConf() {
  const { Base64, Utf8 } = CryptoJS.enc
  // const { data } = await axios.post(
  //   'https://etcd.leiax00.cn/v3/auth/authenticate',
  //   {
  //     name: 'uiUser',
  //     password: '12345678',
  //   }
  // )
  // const headers = { Authorization: data.token }
  // await axios.post('https://etcd.leiax00.cn/v3/kv/put', {
  //   key: Base64.stringify(Utf8.parse('app.ui.ui-main')),
  //   value: Base64.stringify(Utf8.parse(JSON.stringify(settings)))
  // }, { headers })
  // 查询以 app.ui开头的所有服务的配置
  const key = Base64.stringify(
    Utf8.parse(import.meta.env.VITE_APP_CONFIG_ETCD_KEY)
  )
  const resp = await axios.get(`/config/v1/prop/${key}`, {
    params: { prefix: 1 },
  })
  const conf: any = { menus: [], serves: [] }
  resp.data?.data?.kvs.forEach((item: { key: string; value: string }) => {
    const { key, value } = item
    if (key === 'app/ui/common') {
      conf.common = JSON.parse(value)
    }
    if (key.startsWith('app/ui/menu/')) {
      conf.menus.push(...JSON.parse(value))
    }
    if (key.startsWith('app/ui/serve/')) {
      conf.serves.push(JSON.parse(value))
    }
  })
  return Promise.resolve(conf)
}
