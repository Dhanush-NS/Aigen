import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: process.env.NODE_ENV === "production" ? "/AI-Gen/" : "/",
  esbuild: {
    loader: 'jsx',
    include: /src\/.*\.jsx$/, // treat all .js in src as JSX
  },
})
