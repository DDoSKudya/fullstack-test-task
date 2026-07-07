import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{vue,ts}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        primary: {
          DEFAULT: "#2D9B6A",
          hover: "#248F5F",
          soft: "#E8F5EE",
          muted: "#B8DFC9",
        },
        surface: {
          page: "#F8FAF9",
          card: "#FFFFFF",
          elevated: "#FFFFFF",
        },
        text: {
          DEFAULT: "#1A2E24",
          muted: "#6B7F75",
          faint: "#9AADA4",
        },
        warning: "#E5A84B",
        danger: "#E07A6B",
        border: "#E2E8E5",
      },
      borderRadius: {
        xl: "0.75rem",
        "2xl": "1rem",
        "3xl": "1.25rem",
      },
      boxShadow: {
        card: "0 1px 2px rgba(26, 46, 36, 0.04), 0 4px 16px rgba(26, 46, 36, 0.06)",
        "card-hover": "0 4px 8px rgba(26, 46, 36, 0.06), 0 12px 32px rgba(26, 46, 36, 0.1)",
        modal: "0 24px 48px rgba(26, 46, 36, 0.16)",
        glow: "0 0 0 3px rgba(45, 155, 106, 0.15)",
      },
      animation: {
        "fade-in": "fadeIn 0.4s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
      },
      keyframes: {
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        slideUp: {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
