import * as path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import DefineOptions from 'unplugin-vue-define-options/vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import content from '@originjs/vite-plugin-content'
import { FullComponents, SzResolver } from '@leiax00/build'

const resolvePath = (_path) => path.resolve(__dirname, _path)
// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  return {
    resolve: {
      extensions: ['.js', '.ts', '.tsx', '.jsx'],
      alias: {
        '@': resolvePath('src'),
        '~@': resolvePath('src'),
      },
    },
    plugins: [
      vue(),
      vueJsx(),
      DefineOptions(),
      content(),
      AutoImport({
        resolvers: [ElementPlusResolver(), SzResolver()],
      }),
      Components({
        dts: true,
        deep: true,
        resolvers: [
          ElementPlusResolver({
            importStyle: false,
          }),
          SzResolver(),
        ],
      }),
    ],
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "@/styles/element/index.scss";',
        },
      },
    },
    server: {
      host: '0.0.0.0',
      port: 10000,
      strictPort: false, // 端口占用是否进行下一个端口尝试
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
      proxy: {},
    },
  }
})
