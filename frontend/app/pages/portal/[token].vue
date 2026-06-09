<template>
  <div>
    <!-- Show a full-screen loading spinner while validating the token -->
    <div v-if="isValidating" class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <Loader2 class="w-10 h-10 text-indigo-600 animate-spin mb-4" />
      <h2 class="text-xl font-bold text-gray-900">Loading your portal...</h2>
      <p class="text-gray-500 mt-2 text-center max-w-sm">We are securely verifying your magic link.</p>
    </div>
    
    <!-- Show error if token is invalid -->
    <div v-else-if="error" class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div class="bg-white p-8 rounded-3xl shadow-sm border border-red-100 max-w-md w-full text-center">
        <div class="w-16 h-16 bg-red-50 text-red-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <AlertCircle class="w-8 h-8" />
        </div>
        <h2 class="text-2xl font-bold text-gray-900 mb-2">Invalid Link</h2>
        <p class="text-gray-500 mb-6">{{ error }}</p>
        <p class="text-sm text-gray-400">Please ask your freelancer to send you a new portal link.</p>
      </div>
    </div>

    <!-- If validated successfully, render the child routes using NuxtPage -->
    <NuxtPage v-else />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Loader2, AlertCircle } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

// We force this page (and its children) to use the 'portal' layout, not the default freelancer dashboard layout!
definePageMeta({
  layout: 'portal'
})

const route = useRoute()
const token = route.params.token
const api = useApi()

const isValidating = ref(true)
const error = ref(null)

const validateToken = async () => {
  try {
    // This hits the backend, which looks up the token and sets an HttpOnly 'cp_session' cookie in the browser.
    await api('/api/v1/auth/portal/validate', {
      method: 'POST',
      body: { portal_token: token }
    })
    
    // Successfully validated and cookie set! The NuxtPage (index.vue) will now render.
    isValidating.value = false
  } catch (err) {
    console.error('Portal validation failed:', err)
    error.value = 'This magic link has expired or is invalid.'
    isValidating.value = false
  }
}

onMounted(() => {
  validateToken()
})
</script>
