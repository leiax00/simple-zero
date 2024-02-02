export type R<T> = {
  code: number
  msg?: string
  data: T
}

export type User = {
  username: string
  password: string
}
