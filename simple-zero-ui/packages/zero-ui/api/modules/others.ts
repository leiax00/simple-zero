import service from '../service'

export const getYiYan = (params: any): Promise<Record<string, any>> => {
  return service.get('/api/v1/yiy', {
    params,
    headers: {
      needToken: false,
    },
  })
}
