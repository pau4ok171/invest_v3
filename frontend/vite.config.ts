import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    headers: {
      "Content-Security-Policy": "default-src 'self'; " +
        "script-src 'self' 'unsafe-inline'; " +
        "style-src 'self' 'unsafe-inline';" +
        "img-src 'self' data: blob: http://localhost:8000 http://127.0.0.1:8000 http://localhost:5173; " +
        "font-src 'self'; " +
        "object-src 'none';" +
        "connect-src 'self' http://localhost:8000 http://127.0.0.1:8000"
    },
  },
  plugins: [vue(), vuetify({
    styles: {
      configFile: 'src/styles/settings.scss',
    },
  })],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
