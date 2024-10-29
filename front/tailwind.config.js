/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    colors: {
      'calm-green': '#42b883',
    }
  },
  // eslint-disable-next-line no-undef
  plugins: [require("daisyui")],
  // disables deletion of default html styles
  corePlugins: {
    prefligth: false
  }
}

