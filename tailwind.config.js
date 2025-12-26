/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html',
      './**/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui"), require('@tailwindcss/typography')],
  daisyui: {
      themes: ["light", "dark"],
  },
}
