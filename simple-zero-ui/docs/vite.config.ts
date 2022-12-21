import * as path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueMacros from 'unplugin-vue-macros/vite'
import vueJsx from '@vitejs/plugin-vue-jsx'
import content from '@originjs/vite-plugin-content'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Inspect from 'vite-plugin-inspect'
import { SzResolver } from '@leiax00/resolvers'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  resolve: {
    // extensions: ['.js', '.ts', '.tsx', '.jsx'],
    alias: {
      '@/': `${path.resolve(__dirname, 'src')}/`,
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/element/index.scss" as *;`,
      },
    },
  },
  server: getServer(),
  plugins: getPlugins(mode),
}))

function getPlugins(mode: string): any {
  const plugins = [
    VueMacros({
      plugins: {
        vue: vue(),
        vueJsx: vueJsx(),
      },
    }),
    // content(),
    AutoImport({
      imports: ['vue'],
    }),
    Components({
      resolvers: [ElementPlusResolver({ importStyle: 'sass' }), SzResolver()],
    }),
  ]
  if (mode === 'development') {
    plugins.push(Inspect())
  }
  return plugins
}

function getServer() {
  return {
    host: '0.0.0.0',
    port: 3000,
    strictPort: false, // 端口占用是否进行下一个端口尝试
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {},
  }
}
