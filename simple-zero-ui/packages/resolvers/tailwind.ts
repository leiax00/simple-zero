import type { Config } from 'tailwindcss'

const constObj = {
  LOGO_MAX_WIDTH: '150PX',
  RIGHT_NAV_PX: '200px',
}

export const tailwind = {
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
      colors: {
        zinc: {
          '410': '#909399',
        },
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
} satisfies Config
