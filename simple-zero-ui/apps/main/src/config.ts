import CryptoJS from 'crypto-js'
import axios from 'axios'
import type { EtcdConf } from '@/beans'

export async function loadAppConf() {
  const { Base64, Utf8 } = CryptoJS.enc
  // 查询以 app.ui开头的所有服务的配置
  const key = Base64.stringify(Utf8.parse(import.meta.env.VITE_APP_CONFIG_ETCD_KEY))
  const resp = await axios.get(`/api/config/v1/prop/${key}`, {
    params: { prefix: 1 },
  })
  const conf: EtcdConf = { menus: [], serves: [] }
  resp.data?.data?.kvs.forEach((item: { key: string; value: string }) => {
    const { key, value } = item
    let valObj = JSON.parse(value)
    if (key === 'app/ui/common') {
      conf.common = valObj
    }
    valObj = !Array.isArray(valObj) ? [valObj] : valObj
    if (key.startsWith('app/ui/menu/')) {
      conf.menus.push(...valObj)
    }
    if (key.startsWith('app/ui/serve/')) {
      conf.serves.push(...valObj)
    }
  })
  return Promise.resolve(conf)
}
