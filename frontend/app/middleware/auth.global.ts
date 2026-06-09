/**
 * middleware/auth.global.ts
 * 
 * In Nuxt 3, files ending in `.global.ts` inside the `middleware/` directory
 * are executed BEFORE EVERY SINGLE PAGE LOAD automatically.
 * We use this to protect dashboard pages from unauthenticated users.
 */
import { useAuthStore } from '~/stores/auth'
import { defineNuxtRouteMiddleware, navigateTo } from '#app'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // We only run this middleware on the client-side browser
  // Nuxt server-side doesn't have access to localStorage directly without cookie injection
  if (import.meta.client) {
    const authStore = useAuthStore()
    
    // Always make sure the store is initialized (checks localStorage for a token)
    // This is useful if the user hard-refreshed the page
    if (!authStore.isAuthenticated) {
      await authStore.init()
    }

    // Determine what kind of page they are trying to visit
    const isAuthPage = to.path.startsWith('/auth')
    const isPortalPage = to.path.startsWith('/portal') // Client portal is protected by magic links

    // RULE 1: If they are NOT logged in, and trying to access a protected dashboard route, kick them to login
    if (!authStore.isAuthenticated && !isAuthPage && !isPortalPage) {
      return navigateTo('/auth/login')
    }

    // RULE 2: If they ARE logged in, but trying to visit the login page, push them to the dashboard
    if (authStore.isAuthenticated && isAuthPage) {
      return navigateTo('/')
    }
  }
})
