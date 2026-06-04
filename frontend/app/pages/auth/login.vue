<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 flex items-center justify-center p-4 font-sans">
    <!-- A glassmorphism card for the login box -->
    <div class="max-w-md w-full bg-white/80 backdrop-blur-md shadow-xl rounded-2xl p-8 border border-white/50">
      
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-12 h-12 bg-indigo-600 rounded-xl mx-auto flex items-center justify-center shadow-lg mb-4">
          <!-- Temporary logo placeholder -->
          <span class="text-white font-bold text-xl">CP</span>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 tracking-tight">Welcome back</h2>
        <p class="text-sm text-gray-500 mt-2">Sign in to your freelancer dashboard</p>
      </div>

      <!-- The Login Form -->
      <!-- @submit.prevent stops the page from reloading when the user hits enter -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        
        <!-- Email Input -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <div class="mt-1">
            <!-- v-model binds the input to our 'email' reactive variable -->
            <input 
              id="email" 
              v-model="email" 
              type="email" 
              required 
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors"
              placeholder="you@example.com"
            />
          </div>
        </div>

        <!-- Password Input -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <div class="mt-1">
            <!-- v-model binds the input to our 'password' reactive variable -->
            <input 
              id="password" 
              v-model="password" 
              type="password" 
              required 
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors"
            />
          </div>
        </div>

        <!-- Error Message Display -->
        <!-- v-if ensures this div only renders if the authStore has an error -->
        <div v-if="authStore.error" class="rounded-md bg-red-50 p-4 border border-red-200">
          <div class="flex">
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">{{ authStore.error }}</h3>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <div>
          <!-- :disabled prevents clicking while the API is loading -->
          <button 
            type="submit" 
            :disabled="authStore.isLoading"
            class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <!-- Show "Signing in..." if loading, else show "Sign in" -->
            {{ authStore.isLoading ? 'Signing in...' : 'Sign in' }}
          </button>
        </div>
      </form>
      
    </div>
  </div>
</template>

<script setup>
/**
 * Vue 3 Composition API setup script.
 * Code here runs once when the component is created.
 */
import { ref } from 'vue'
import { useRouter } from '#app' // Nuxt router to handle navigation
import { useAuthStore } from '~/stores/auth'

// Tell Nuxt NOT to use the default layout (which has the dashboard sidebar)
// We want the login page to take up the full screen!
definePageMeta({
  layout: false
})

// Initialize our tools
const authStore = useAuthStore()
const router = useRouter()

// Reactive variables for the form inputs
// 'ref' makes them reactive, meaning the UI automatically updates when their values change
const email = ref('')
const password = ref('')

/**
 * Handles the form submission.
 * Calls the login action in our Pinia store.
 */
const handleLogin = async () => {
  // Try to log in
  const success = await authStore.login({
    email: email.value,
    password: password.value
  })

  // If successful, redirect them to the root dashboard page!
  if (success) {
    router.push('/')
  }
}
</script>
