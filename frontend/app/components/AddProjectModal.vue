<template>
  <!-- Modal Backdrop -->
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm" @click.self="close">
    
    <!-- Modal Content -->
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden transform transition-all">
      <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <h3 class="text-lg font-bold text-gray-900">Create New Project</h3>
        <button @click="close" class="text-gray-400 hover:text-gray-600 transition-colors">
          <X class="w-5 h-5" />
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <!-- Error Message -->
        <div v-if="error" class="p-3 bg-red-50 text-red-700 text-sm rounded-lg border border-red-100 mb-4">
          {{ error }}
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Project Name *</label>
          <input v-model="form.name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Website Redesign" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Assign to Client *</label>
          <div class="relative">
            <select v-model="form.client_id" required class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm appearance-none bg-white">
              <option value="" disabled selected>Select a client...</option>
              <option v-for="client in clients" :key="client.id" :value="client.id">
                {{ client.name }} <span v-if="client.company_name">({{ client.company_name }})</span>
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
              <ChevronDown class="w-4 h-4" />
            </div>
          </div>
          <!-- Show a link to create a client if the list is empty -->
          <p v-if="!isLoadingClients && clients.length === 0" class="mt-1 text-xs text-red-500">
            You must <NuxtLink to="/clients" class="underline hover:text-red-700">create a client</NuxtLink> before adding a project.
          </p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description <span class="text-gray-400 font-normal">(Optional)</span></label>
          <textarea v-model="form.description" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm resize-none" placeholder="Brief details about the project..."></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Default Hourly Rate <span class="text-gray-400 font-normal">(Optional)</span></label>
          <div class="relative mt-1 rounded-md shadow-sm">
            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <span class="text-gray-500 sm:text-sm">$</span>
            </div>
            <!-- Input binds to string but we'll convert to cents on submit -->
            <input v-model="form.hourly_rate" type="number" min="0" step="1" class="block w-full rounded-lg border-gray-300 pl-7 pr-12 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 border" placeholder="0.00" />
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
              <span class="text-gray-500 sm:text-sm">USD</span>
            </div>
          </div>
        </div>

        <div class="mt-6 flex gap-3 justify-end">
          <button type="button" @click="close" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Cancel
          </button>
          <button type="submit" :disabled="isLoading || clients.length === 0" class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center">
            <Loader2 v-if="isLoading" class="w-4 h-4 mr-2 animate-spin" />
            <span v-if="!isLoading">Create Project</span>
            <span v-else>Creating...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { X, Loader2, ChevronDown } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

const props = defineProps({
  isOpen: Boolean
})
const emit = defineEmits(['close', 'project-added'])

const api = useApi()

// Form state
const form = ref({
  name: '',
  client_id: '',
  description: '',
  hourly_rate: ''
})
const isLoading = ref(false)
const error = ref(null)

// Client fetching state
const clients = ref([])
const isLoadingClients = ref(false)

const close = () => {
  error.value = null
  form.value = { name: '', client_id: '', description: '', hourly_rate: '' }
  emit('close')
}

// Fetch clients whenever the modal is opened
watch(() => props.isOpen, async (newVal) => {
  if (newVal) {
    await fetchClients()
  }
})

const fetchClients = async () => {
  isLoadingClients.value = true
  try {
    const data = await api('/api/v1/clients')
    clients.value = data
  } catch (err) {
    console.error('Failed to fetch clients', err)
  } finally {
    isLoadingClients.value = false
  }
}

const handleSubmit = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Convert hourly rate from dollars to cents for the backend
    const cents = form.value.hourly_rate ? parseInt(parseFloat(form.value.hourly_rate) * 100) : null

    const response = await api('/api/v1/projects', {
      method: 'POST',
      body: {
        name: form.value.name,
        client_id: form.value.client_id,
        description: form.value.description || null,
        default_hourly_rate_cents: cents
      }
    })
    
    emit('project-added', response)
    close()
  } catch (err) {
    error.value = err.data?.detail || 'Failed to create project. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>
