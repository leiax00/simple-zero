/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      width: (() => {
        const sizeList = [150, 500]
        const tmp = {}
        sizeList.forEach(item => {
          tmp[`sz-${item}`] = `${item}px !important`
        })
        return tmp
      })()
    },
  },
  plugins: [],
}
