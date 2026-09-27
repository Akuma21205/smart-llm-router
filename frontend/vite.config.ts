import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/stats': 'http://localhost:8000',
      '/telemetry': 'http://localhost:8000',
      '/chat': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
      '/v1': 'http://localhost:8000',
    },
  },
})
