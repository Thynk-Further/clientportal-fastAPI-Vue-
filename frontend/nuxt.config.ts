// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxtjs/google-fonts'
  ],
  googleFonts: {
    families: {
      'Hanken+Grotesk': [600, 700],
      'Inter': [400, 500, 600],
      'JetBrains+Mono': [500]
    }
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000'
    }
  }
})
