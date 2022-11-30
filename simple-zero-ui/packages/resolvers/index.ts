import type { ComponentResolver } from 'unplugin-vue-components/types'

export const SzResolver = function (): ComponentResolver[] {
  return [
    {
      type: 'component',
      resolve: async (name: string) => {
        if (name.toLowerCase().startsWith('sz')) {
          return {
            name,
            from: '@leiax00/zero-ui',
          }
        }
      },
    },
    {
      type: 'directive',
      resolve: async (name: string) => {
        return {
          name,
          from: '@leiax00/zero-ui',
        }
      },
    },
  ]
}
export default {}
