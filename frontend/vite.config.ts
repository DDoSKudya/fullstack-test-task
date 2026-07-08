import vue from "@vitejs/plugin-vue";
import path from "node:path";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const proxyTarget = env.VITE_PROXY_TARGET || "http://localhost:8000";

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
    test: {
      environment: "happy-dom",
      include: ["src/**/*.test.ts"],
      coverage: {
        provider: "v8",
        include: [
          "src/api/**/*.ts",
          "src/composables/**/*.ts",
          "src/utils/**/*.ts",
          "src/i18n/index.ts",
        ],
        exclude: ["**/*.test.ts", "src/types/**"],
        thresholds: {
          lines: 85,
          functions: 85,
          statements: 85,
          branches: 85,
        },
      },
    },
    server: {
      host: true,
      port: 3000,
      proxy: {
        "/api": {
          target: proxyTarget,
          changeOrigin: true,
        },
      },
    },
  };
});
