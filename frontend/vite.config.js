import { defineConfig } from 'vite'
import svelte from 'vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 5173,
    open: true
  }
})
