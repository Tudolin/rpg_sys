import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// The Flask app serves the built SPA from frontend/dist, its game assets
// (monster art, music, uploads) from /static, the JSON API from /api and
// the realtime channel from /socket.io. In dev, Vite proxies those three
// to Flask so the SPA behaves identically to production.
const FLASK_ORIGIN = process.env.FLASK_ORIGIN ?? "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [
    vue({
      // Caminhos absolutos (/static/...) são assets servidos pelo Flask em
      // runtime — retratos, músicas, arte de monstros. O bundler não deve
      // tentar resolvê-los em tempo de build.
      template: { transformAssetUrls: { includeAbsolute: false } },
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: false,
  },
  server: {
    port: 5173,
    proxy: {
      "/api": { target: FLASK_ORIGIN, changeOrigin: true },
      "/static": { target: FLASK_ORIGIN, changeOrigin: true },
      "/socket.io": { target: FLASK_ORIGIN, ws: true, changeOrigin: true },
    },
  },
});
