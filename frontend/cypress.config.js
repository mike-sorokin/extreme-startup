import { defineConfig } from 'cypress'

export default defineConfig({
  env: {
    baseUrl: 'http://localhost:5173/'
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite'
    }
  },
  e2e: {
    setupNodeEvents (on, config) {
      // implement node event listeners here
    },
    experimentalStudio: true
  }
})
