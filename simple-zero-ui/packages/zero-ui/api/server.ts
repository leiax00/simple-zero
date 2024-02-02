import service from './service'
import type { User } from './domain'

export const login = (user: User): Promise<{ expire: number; token: string }> => {
  return service.post('/api/auth/v1/login', user, {
    headers: {
      needToken: false,
    },
  })
}
export const logout = (): Promise<any> => {
  return service.delete('/api/auth/v1/logout')
}

export default {}
