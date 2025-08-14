import path from "path"

import { defineConfig } from "vite"
import { minify } from "html-minifier-terser"
import { svelte } from "@sveltejs/vite-plugin-svelte"
import legacy from "@vitejs/plugin-legacy"

export default defineConfig({
  plugins: [
    svelte(),
    legacy({
      targets: ["defaults", "not IE 11"],
    }),
    {
      name: "html-minifier-terser",
      apply: "build",
      transformIndexHtml: {
        order: "post",
        handler(html) {
          return minify(html, {
            removeComments: true,
            removeRedundantAttributes: true,
            removeScriptTypeAttributes: true,
            removeStyleLinkTypeAttributes: true,
            useShortDoctype: true,
            minifyCSS: true,
            minifyJS: true,
            collapseWhitespace: true,
            conservativeCollapse: false, // remove all unnecessary whitespaces
            caseSensitive: true,
            keepClosingSlash: true,
            removeEmptyAttributes: true,
            sortAttributes: true,
            sortClassName: true,
          })
        },
      },
    },
  ],
  build: {
    outDir: "target",
    emptyOutDir: true,
    // More aggressive minification settings
    minify: "terser", // 'esbuild''
    terserOptions: {
      compress: {
        arguments: true,
        booleans_as_integers: true,
        drop_console: false, // Keep console statements for debugging
        drop_debugger: true,
        passes: 3,
        unsafe: true,
        unsafe_arrows: true,
        unsafe_comps: true,
        unsafe_math: true,
        unsafe_proto: true,
      },
      mangle: {
        properties: {
          regex: /^_/, // Mangle private properties
        },
      },
    },
  },
  server: {
    open: "/index.html",
  },

  resolve: {
    alias: {
      "murmuring-boids": path.resolve(__dirname, "components/murmuring-boids.link"),
    },
  },
})
