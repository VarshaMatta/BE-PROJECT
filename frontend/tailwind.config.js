/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0B0E17',       // Main deep dark backdrop
          card: '#121726',     // Card surface
          cardHover: '#181E30',
          border: '#1E293B',   // Dark border
          input: '#151A2C',
        },
        brand: {
          50: '#F5F3FF',
          100: '#EDE9FE',
          500: '#8B5CF6',
          600: '#7C3AED',
          700: '#6D28D9',
          800: '#5B21B6',
          900: '#4C1D95',
        }
      }
    },
  },
  plugins: [],
}
