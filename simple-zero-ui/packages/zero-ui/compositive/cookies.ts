import { useCookies } from '@vueuse/integrations/useCookies'

const cookies = useCookies()

const TokenKey = 'AT'
const ExpiresInKey = 'AEI'

export function getToken(): string {
  return cookies.get(TokenKey)
}

export function setToken(token: string) {
  return cookies.set(TokenKey, token)
}

export function removeToken() {
  return cookies.remove(TokenKey)
}

export function getExpiresIn() {
  return cookies.get(ExpiresInKey) || -1
}

export function setExpiresIn(time: number) {
  return cookies.set(ExpiresInKey, time)
}

export function removeExpiresIn() {
  return cookies.remove(ExpiresInKey)
}
