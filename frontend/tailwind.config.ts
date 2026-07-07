import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{vue,ts}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        text: {
          muted: "#6B7F75",
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
