<template>
  <!-- Modal Backdrop -->
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm" @click.self="close">
    
    <!-- Modal Content -->
    <div class="bg-layer-1 border border-white/10 rounded-2xl shadow-xl w-full max-w-md overflow-hidden transform transition-all">
      <div class="px-6 py-4 border-b border-white/5 flex items-center justify-between">
        <h3 class="text-lg font-bold text-white font-heading">Add New Client</h3>
        <button @click="close" class="text-gray-500 hover:text-gray-300 transition-colors">
          <X class="w-5 h-5" />
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <!-- Error Message -->
        <div v-if="error" class="p-3 bg-red-900/20 text-red-400 text-sm rounded-lg border border-red-900/50 mb-4">
          {{ error }}
        </div>

        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1">Full Name *</label>
          <input v-model="form.name" type="text" required class="w-full px-3 py-2 bg-layer-2 border border-white/10 text-white rounded-lg shadow-sm focus:ring-accent focus:border-accent sm:text-sm placeholder-gray-500" placeholder="Jane Doe" />
        </div>

        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1">Email Address *</label>
          <input v-model="form.email" type="email" required class="w-full px-3 py-2 bg-layer-2 border border-white/10 text-white rounded-lg shadow-sm focus:ring-accent focus:border-accent sm:text-sm placeholder-gray-500" placeholder="jane@example.com" />
        </div>

        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1">Company Name <span class="text-gray-500 font-normal">(Optional)</span></label>
          <input v-model="form.company_name" type="text" class="w-full px-3 py-2 bg-layer-2 border border-white/10 text-white rounded-lg shadow-sm focus:ring-accent focus:border-accent sm:text-sm placeholder-gray-500" placeholder="Acme Corp" />
        </div>

        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1">Phone Number <span class="text-gray-500 font-normal">(Optional)</span></label>
          <input v-model="form.phone" type="text" class="w-full px-3 py-2 bg-layer-2 border border-white/10 text-white rounded-lg shadow-sm focus:ring-accent focus:border-accent sm:text-sm placeholder-gray-500" placeholder="+1 (555) 000-0000" />
        </div>

        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1">Address <span class="text-gray-500 font-normal">(Optional)</span></label>
          <input v-model="form.address" type="text" class="w-full px-3 py-2 bg-layer-2 border border-white/10 text-white rounded-lg shadow-sm focus:ring-accent focus:border-accent sm:text-sm placeholder-gray-500" placeholder="123 Main St, City, Country" />
        </div>

        <div class="mt-6 flex gap-3 justify-end">
          <button type="button" @click="close" class="px-4 py-2 text-sm font-medium text-gray-300 bg-layer-2 border border-white/10 rounded-lg hover:bg-[#2e2e2e] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent">
            Cancel
          </button>
          <button type="submit" :disabled="isLoading" class="px-4 py-2 text-sm font-medium text-layer-0 bg-accent rounded-lg hover:bg-[#a4d64c] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50 disabled:cursor-not-allowed flex items-center">
            <Loader2 v-if="isLoading" class="w-4 h-4 mr-2 animate-spin text-layer-0" />
            <span v-if="!isLoading">Add Client</span>
            <span v-else>Adding...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { X, Loader2 } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

// Props and Emits
const props = defineProps({
  isOpen: Boolean
})
const emit = defineEmits(['close', 'client-added'])

const api = useApi()

// Form state
const form = ref({
  name: '',
  email: '',
  company_name: '',
  phone: '',
  address: ''
})
const isLoading = ref(false)
const error = ref(null)

const close = () => {
  error.value = null
  form.value = { name: '', email: '', company_name: '', phone: '', address: '' }
  emit('close')
}

const handleSubmit = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await api('/api/v1/clients', {
      method: 'POST',
      body: {
        name: form.value.name,
        email: form.value.email,
        company_name: form.value.company_name || null,
        phone: form.value.phone || null,
        address: form.value.address || null
      }
    })
    
    // Successfully created! The backend just sent them an email via Resend.
    emit('client-added', response)
    close()
  } catch (err) {
    error.value = err.data?.detail || 'Failed to add client. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>
