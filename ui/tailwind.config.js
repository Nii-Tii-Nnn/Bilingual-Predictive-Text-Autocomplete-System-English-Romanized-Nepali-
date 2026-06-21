export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#0a0a0a',
        'surface': '#111111',
        'card': '#141414',
        'border': '#2a2a2a',
        'text-primary': '#ffffff',
        'text-muted': '#666666',
        'accent-purple': '#534ab7',
        'accent-purple-light': '#afa9ec',
      },
      fontFamily: {
        'system': 'system-ui, -apple-system, sans-serif',
      }
    },
  },
  plugins: [],
}
