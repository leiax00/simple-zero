import * as path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import Inspect from 'vite-plugin-inspect'
import content from '@originjs/vite-plugin-content'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { SzResolver } from '@leiax00/resolvers'
import viteCompression from 'vite-plugin-compression'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
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
        additionalData: `
        @use "@leiax00/zero-ui/styles/element/index.scss" as *;
        `,
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
    content(),
    AutoImport({
      imports: ['vue', 'vue-router'],
    }),
    Components({
      resolvers: [ElementPlusResolver({ importStyle: 'sass' }), SzResolver()],
    }),
    viteCompression({ threshold: 100 * 1024 }), // > 100kb则压缩
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
    proxy: {
      '/api/': {
        target: 'https://leiax00.cn',
        changeOrigin: true,
      },
    },
  }
}
