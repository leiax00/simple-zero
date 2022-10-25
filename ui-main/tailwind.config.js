const constObj = {
  LOGO_MAX_WIDTH: '150PX',
  RIGHT_NAV_PX: '200px'
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  // darkMode: false,
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      maxWidth: {
        logo: constObj.LOGO_MAX_WIDTH,
        'px-200': constObj.RIGHT_NAV_PX
      },
      flex: {
        logo: `0 0 ${constObj.LOGO_MAX_WIDTH}`,
        'px-200': `0 0 ${constObj.RIGHT_NAV_PX}`
      }
    }
  },
  variants: {
    extend: {}
  },
  plugins: []
}
