/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        agro: {
          50: '#f2f9f4',
          100: '#e1f2e6',
          200: '#c4e6ce',
          300: '#97d2aa',
          400: '#64b680',
          500: '#3f9a5e',
          600: '#2f7c49',
          700: '#27633c',
          800: '#234f32',
          900: '#1e412b',
          950: '#0c2316',
        },
        earth: {
          50: '#faf6f0',
          100: '#f4ede0',
          200: '#e9dac1',
          300: '#dbc09d',
          400: '#cba378',
          500: '#be8c5c',
          600: '#b0774f',
          700: '#935e41',
          800: '#774c38',
          900: '#613f30',
        },
        cream: '#fbfbf7',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03)',
        'card': '0 4px 20px -2px rgba(14, 56, 32, 0.08)',
        'glow': '0 0 20px rgba(34, 197, 94, 0.25)',
      }
    },
  },
  plugins: [],
}
