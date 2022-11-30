import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import DefineOptions from 'unplugin-vue-define-options/vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import qiankun from 'vite-plugin-qiankun'
import { FullComponents, SzResolver } from '@leiax00/build'
// @ts-ignore
import pkgInfo from './package.json'

const resolvePath = (_path: string) => resolve(__dirname, _path)

export default defineConfig(({ mode }) => {
  return {
    base: '/',
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
      AutoImport({
        resolvers: [ElementPlusResolver(), SzResolver()],
      }),
      mode === 'development'
        ? FullComponents()
        : Components({
            resolvers: [
              ElementPlusResolver({
                importStyle: false,
              }),
              SzResolver(),
            ],
          }),
      qiankun(pkgInfo.name, {
        useDevMode: true,
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
      port: 10001,
      strictPort: false, // 端口占用是否进行下一个端口尝试
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
      proxy: {
        '/novel/v1/api/': {
          target: 'http://10.1.0.4:11000/',
          changeOrigin: true,
        },
      },
    },
  }
})
