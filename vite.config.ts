import { defineConfig } from "vite"
import { svelte } from "@sveltejs/vite-plugin-svelte"
import path from "path"

export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: "target",
    emptyOutDir: true,
  },
  server: {
    open: "/index.html"
  },

  resolve: {
    alias: {
      'murmuring-boids': path.resolve(__dirname, 'components/murmuring-boids'),
    },
  },
})
