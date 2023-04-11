/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  corePlugins: {
    preflight: false,
  },
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {},
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
