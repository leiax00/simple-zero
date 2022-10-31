import CryptoJS from 'crypto-js'
import axios from 'axios'

export async function loadAppConf() {
  const { Base64, Utf8 } = CryptoJS.enc
  const { data } = await axios.post('https://etcd.leiax00.cn/v3/auth/authenticate', {
    name: 'uiUser',
    password: '12345678'
  })
  const headers = { Authorization: data.token }
  // await axios.post('https://etcd.leiax00.cn/v3/kv/put', {
  //   key: Base64.stringify(Utf8.parse('app.ui.ui-main')),
  //   value: Base64.stringify(Utf8.parse(JSON.stringify(settings)))
  // }, { headers })
  // 查询以 app.ui开头的所有服务的配置
  const resp = await axios.post('https://etcd.leiax00.cn/v3/kv/range', {
    key: Base64.stringify(Utf8.parse('app.ui.ui-main'))
    // range_end: Base64.stringify(Utf8.parse('app.ui' + 1))
  }, { headers })
  let conf = {}
  if (resp.data.kvs) {
    const confStr = Utf8.stringify(Base64.parse(resp.data.kvs[0].value))
    conf = JSON.parse(confStr)
  }
  return Promise.resolve(conf)
}
