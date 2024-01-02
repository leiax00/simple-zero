import service from './server'
import type { User } from './domain'

export const login = (user: User) => {
  return service.post('/api/auth/v1/login', user)
}

export default {}
