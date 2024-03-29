import * as path from 'path'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import Inspect from 'vite-plugin-inspect'
import content from '@originjs/vite-plugin-content'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { SzResolver } from '@leiax00/resolvers'
import qiankun from 'vite-plugin-qiankun'
import viteCompression from 'vite-plugin-compression'
// @ts-ignore
import pkgInfo from './package.json'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    base: mode === 'development' ? '/novel' : loadEnv(mode, process.cwd()).VITE_APP_DOMAIN,
    resolve: {
      // extensions: ['.js', '.ts', '.tsx', '.jsx'],
      alias: {
        '@/': `${path.resolve(__dirname, 'src')}/`,
        '@leiax00/': `${path.resolve(__dirname, '../../packages')}/`,
      },
    },
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@leiax00/zero-ui/styles/element/index.scss" as *;`,
        },
      },
    },
    plugins: getPlugins(mode),
    server: getServer(Number.parseInt(env.APP_PORT)),
  }
})

function getPlugins(mode: string): any {
  const plugins = [
    vue(),
    vueJsx(),
    content(),
    AutoImport({
      imports: ['vue', 'vue-router'],
    }),
    Components({
      resolvers: [ElementPlusResolver({ importStyle: 'sass' }), SzResolver()],
    }),
    qiankun(pkgInfo.name, {
      useDevMode: true,
    }),
    viteCompression({ threshold: 100 * 1024 }), // > 100kb则压缩
  ]
  if (mode === 'development') {
    plugins.push(Inspect())
  }
  return plugins
}

function getServer(port = 80) {
  return {
    host: '0.0.0.0',
    port,
    strictPort: false, // 端口占用是否进行下一个端口尝试
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '/api/novel/v1/': {
        target: 'https://leiax00.cn',
        changeOrigin: true,
      },
    },
  }
}
