import type { SFCWithInstall } from './typescript'

export const withInstall = <T, E extends Record<string, any>>(
  main: T,
  extra?: E
) => {
  ;(main as SFCWithInstall<T>).install = (app): void => {
    for (const comp of [main, ...Object.values(extra ?? {})]) {
      app.component(comp.name, comp)
    }
  }

  if (extra) {
    for (const [key, comp] of Object.entries(extra)) {
      ;(main as any)[key] = comp
    }
  }
  return main as SFCWithInstall<T> & E
}

export const withNoopInstall = <T>(component: T) => {
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  ;(component as SFCWithInstall<T>).install = () => {}

  return component as SFCWithInstall<T>
}
