/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './src/templates/**/*.html',
      './src/**/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui"), require('@tailwindcss/typography')],
  daisyui: {
      themes: ["light", "dark"],
  },
}
