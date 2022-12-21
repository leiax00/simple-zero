import * as path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import DefineOptions from 'unplugin-vue-define-options/vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import Inspect from 'vite-plugin-inspect'
import content from '@originjs/vite-plugin-content'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
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
  plugins: getPlugins(mode),
  server: getServer(),
}))

function getPlugins(mode: string): any {
  const plugins = [
    vue(),
    vueJsx(),
    DefineOptions(),
    content(),
    AutoImport({
      imports: ['vue', 'vue-router'],
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
    port: 10000,
    strictPort: false, // 端口占用是否进行下一个端口尝试
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {},
  }
}
