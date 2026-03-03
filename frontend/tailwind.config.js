/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        arabic: ['"Noto Sans Arabic"', 'sans-serif'],
      },
      colors: {
        ufc: {
          red: '#D20A0A',
          gold: '#C5A44E',
          dark: '#1A1A2E',
          darker: '#0F0F1A',
        },
      },
    },
  },
  plugins: [],
}
