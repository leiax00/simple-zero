import { INSTALLED_KEY } from '@leiax00/constants'
import { SzIcon } from './component'
import { name, version } from './version'
import type { App, Plugin } from '@vue/runtime-core'

export const makeInstaller = (components: Plugin[] = []) => {
  const install = (app: App) => {
    if (app[INSTALLED_KEY]) return

    app[INSTALLED_KEY] = true
    components.forEach((c) => app.use(c))
  }

  return {
    name,
    version,
    install,
  }
}

const plugins = [SzIcon] as Plugin[]
export default makeInstaller(plugins)
