import * as path from 'path'
import * as fs from 'fs'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import dts from 'vite-plugin-dts'
import VueMacros from 'unplugin-vue-macros/vite'

const resolve = (...uri: string[]) => {
  return path.resolve(__dirname, ...uri)
}
const join = (...uri: string[]) => {
  return path.join(...uri)
}
const rootDir = resolve('../../')

const pkgName = 'uiResolvers'
const outputDir = resolve('dist')
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    VueMacros({
      plugins: {
        vue: vue(),
      },
    }),
    dts({
      outputDir: [join(outputDir, 'es')],
      afterBuild: mergeDts,
    }),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        javascriptEnabled: true,
      },
    },
  },
  resolve: {
    alias: {
      '@leiax00': resolve('../'),
    },
  },
  build: {
    target: 'modules',
    //打包文件目录
    outDir: outputDir,
    //压缩
    minify: false,
    //css分离
    //cssCodeSplit: true,
    lib: {
      entry: resolve('index.ts'),
      name: pkgName,
      formats: ['es', 'cjs', 'umd'],
      // fileName: (format) => `index.${format}.js`,
    },
    rollupOptions: {
      // 确保外部化处理那些你不想打包进库的依赖
      external: ['vue'],
      input: resolve('index.ts'),
      output: [
        {
          format: 'es',
          exports: 'auto',
          globals: { vue: 'Vue' },
          //配置打包根目录
          dir: join(outputDir, 'es'),
          //让打包目录和我们目录对应
          preserveModules: true,
          preserveModulesRoot: resolve(),
          //不用打包成.es.js,这里我们想把它打包成.js
          entryFileNames: '[name].mjs',
        },
        {
          format: 'cjs',
          exports: 'named',
          globals: { vue: 'Vue' },
          //配置打包根目录
          dir: join(outputDir, 'lib'),
          //让打包目录和我们目录对应
          preserveModules: true,
          preserveModulesRoot: resolve(),
          entryFileNames: '[name].js',
        },
        {
          format: 'umd',
          exports: 'named',
          globals: { vue: 'Vue' },
          //配置打包根目录
          dir: join(outputDir, 'umd'),
          entryFileNames: '[name].js',
        },
      ],
    },
  },
})

function mergeDts() {
  // 暂时在dts后copy一份package.json到构建目录
  fs.copyFileSync(resolve('package.json'), join(outputDir, 'package.json'))
}
