import { INSTALLED_KEY } from '@leiax00/constants'
import { name as selfName, version } from './package.json'

import type { App, Plugin } from '@vue/runtime-core'

export const makeInstaller = (components: Plugin[] = []) => {
  const install = (app: App) => {
    if (app[INSTALLED_KEY]) return

    app[INSTALLED_KEY] = true
    components.forEach((c) => app.use(c))
  }

  return {
    selfName,
    version,
    install,
  }
}
export default {}
