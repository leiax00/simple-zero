export type Engin = {
  key: string
  label: string
  uri: string
  awake: string
  placeholder: string
}

export type EnginManager = {
  active: string
  enginList: Engin[]
}
