const constObj = {
  LOGO_MAX_WIDTH: '150PX',
  RIGHT_NAV_PX: '200px',
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  corePlugins: {
    preflight: false,
  },
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      maxWidth: {
        logo: constObj.LOGO_MAX_WIDTH,
        'px-200': constObj.RIGHT_NAV_PX,
      },
      flex: {
        logo: `0 0 ${constObj.LOGO_MAX_WIDTH}`,
        'px-200': `0 0 ${constObj.RIGHT_NAV_PX}`,
      },
      boxShadow: {
        'aside-red-right': '2px 0 8px -4px red',
        'aside-red-top': '0 -2px 8px -4px red',
      },
      width: {
        'sz-160': '160px',
        'sz-240': '240px',
        'sz-500': '500px',
      },
      height: {
        'sz-212': '212px',
      },
    },
    screens: {
      sm: '640px',
      md: '992px',
      lg: '1280px',
      xl: '1920px',
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
