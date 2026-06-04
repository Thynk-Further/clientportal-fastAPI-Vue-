/**
 * composables/useApi.ts
 * 
 * In Nuxt 3, anything inside the `composables/` directory is auto-imported.
 * This means we can use `useApi()` anywhere in our Vue components without needing to import it!
 * 
 * This composable is a wrapper around Nuxt's native `$fetch` function.
 * It automatically attaches our base URL (from the backend) and our JWT token (if we are logged in).
 */
import { useRuntimeConfig } from '#app'

export const useApi = () => {
  // Grab the runtime config we defined in nuxt.config.ts
  const config = useRuntimeConfig()
  
  // Create a custom fetch instance with default options
  const customFetch = $fetch.create({
    baseURL: config.public.apiBaseUrl as string,
    
    // onRequest runs right BEFORE the request is sent to the backend
    onRequest({ request, options }) {
      // Look for a token in local storage (only works on the client-side browser)
      // Nuxt is SSR (Server Side Rendered) by default, so we must check if we're in the browser
      if (import.meta.client) {
        const token = localStorage.getItem('access_token')
        
        // If we have a token, inject it into the Authorization header
        if (token) {
          options.headers = new Headers(options.headers || {})
          options.headers.set('Authorization', `Bearer ${token}`)
        }
      }
    },
    
    // onResponseError runs when the backend throws an error (like a 401 Unauthorized)
    onResponseError({ request, response, options }) {
      // If we get a 401, it means our token is expired or invalid.
      if (response.status === 401 && import.meta.client) {
        // Clear the bad token from local storage
        localStorage.removeItem('access_token')
        
        // Redirect the user back to the login page so they can re-authenticate
        // Using window.location forces a hard reload, ensuring Pinia state resets
        if (window.location.pathname !== '/auth/login') {
          window.location.href = '/auth/login'
        }
      }
    }
  })

  return customFetch
}
