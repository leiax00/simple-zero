import * as path from 'path'
import type { Plugin, ResolvedConfig } from 'vite'

export type ComponentsRule = {
  varName?: string
  importList: string[]
  mountFn?: (string) => string
}

const defaultRules: ComponentsRule[] = [
  {
    importList: [
      `import ElementPlus from 'element-plus'`,
      `import 'element-plus/dist/index.css'`,
    ],
    mountFn: (code: string) =>
      code.replace('.mount(', ($1) => `.use(ElementPlus)${$1}`),
  },
  {
    importList: [
      `import { Ripple, default as ZeroUi } from '@leiax00/zero-ui'`,
    ],
    mountFn: (code: string) => {
      code = code.replace(
        '.mount(',
        ($1) => `.use(ZeroUi).directive('ripple', Ripple)${$1}`
      )
      return code
    },
  },
]

export const FullComponents = (rules?: ComponentsRule[]) => {
  rules = rules || defaultRules
  let config: ResolvedConfig
  return <Plugin>{
    name: 'fullLoadComponents',
    async configResolved(conf) {
      config = conf
    },
    transform(code, id) {
      // 判断当前处理的是否是 _src/main.ts_
      if (id.endsWith('src/main.ts')) {
        for (const rule of rules) {
          code = `${rule.importList.join('\n')}\n${code}`
          if (rule.mountFn) {
            code = rule.mountFn(code)
          }
        }
      }
      return code
    },
  }
}
