import { reactive } from 'vue'
import { isEmptyStr } from '@leiax00/utils'
import { getExpiresIn, getToken, removeExpiresIn, removeToken, setExpiresIn, setToken } from '@leiax00/zero-ui'
import { login, logout } from '@leiax00/zero-ui/api'
import { defineStore } from 'pinia'
import type { User } from '@leiax00/zero-ui/api'

export const useServe = defineStore('serve', () => {
  const authInfo = reactive({
    expire: getExpiresIn(),
    token: getToken(),
  })

  const isLogin = computed(() => !isEmptyStr(authInfo.token))

  function loginWeb(user: User): Promise<boolean> {
    return new Promise((resolve, reject) => {
      login(user).then(
        (data) => {
          setToken(data.token)
          setExpiresIn(data.expire)
          authInfo.expire = data.expire
          authInfo.token = data.token
          resolve(true)
        },
        () => reject(false)
      )
    })
  }

  function logoutWeb(): Promise<boolean> {
    return new Promise((resolve) => {
      logout().then(
        () => {
          removeToken()
          removeExpiresIn()
          authInfo.expire = getExpiresIn()
          authInfo.token = getToken()
          resolve(true)
        },
        () => {
          resolve(false)
        }
      )
    })
  }
  return {
    authInfo,
    isLogin,
    loginWeb,
    logoutWeb,
  }
})
