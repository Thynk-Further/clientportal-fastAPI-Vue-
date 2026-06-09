/**
 * stores/auth.ts
 * 
 * This is a Pinia store. Pinia is the official state management library for Vue 3.
 * It acts like a global "brain" or "database" for the frontend.
 * Any component can read from or write to this store, making it perfect for Authentication state.
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // ==========================================
  // STATE (Data we want to track globally)
  // ==========================================
  
  // The currently logged-in user. Starts as null.
  const user = ref<any>(null)
  
  // Whether we are currently making an API request (useful for showing loading spinners)
  const isLoading = ref<boolean>(false)
  
  // Any error messages that happen during auth (e.g., "Invalid password")
  const error = ref<string | null>(null)
  
  // A boolean to quickly check if someone is logged in
  const isAuthenticated = ref<boolean>(false)

  // ==========================================
  // ACTIONS (Functions that modify the state)
  // ==========================================

  /**
   * Initializes the store when the app loads.
   * It checks local storage for a token and fetches the user profile if one exists.
   */
  const init = async () => {
    if (import.meta.client) {
      const token = localStorage.getItem('access_token')
      if (token) {
        isAuthenticated.value = true
        await fetchUser()
      }
    }
  }

  /**
   * Attempts to log the user in using email and password.
   */
  const login = async (credentials: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      // Our FastAPI /login endpoint expects a JSON payload matching the LoginRequest schema
      const api = useApi()
      const response = await api('/api/v1/auth/login', {
        method: 'POST',
        body: {
          email: credentials.email,
          password: credentials.password
        }
      }) as any
      
      // If successful, save the token to local storage
      if (response && response.access_token) {
        localStorage.setItem('access_token', response.access_token)
        isAuthenticated.value = true
        
        // Fetch their profile data immediately after login
        await fetchUser()
        return true
      }
      return false
    } catch (e: any) {
      // If the backend rejects the login (e.g., wrong password), capture the error from the response payload
      error.value = e.data?.detail || 'Invalid email or password'
      return false
    } finally {
      // Always stop the loading spinner, regardless of success or failure
      isLoading.value = false
    }
  }

  /**
   * Fetches the current user's profile from the backend using the stored token.
   */
  const fetchUser = async () => {
    try {
      const api = useApi()
      const response = await api('/api/v1/users/me')
      user.value = response
    } catch (e) {
      // If fetching fails (e.g., token expired), wipe the state completely
      logout()
    }
  }

  /**
   * Logs the user out by wiping the token and state.
   */
  const logout = () => {
    user.value = null
    isAuthenticated.value = false
    if (import.meta.client) {
      localStorage.removeItem('access_token')
    }
  }

  // We MUST return the state and actions so our Vue components can access them!
  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    init,
    login,
    fetchUser,
    logout
  }
})
