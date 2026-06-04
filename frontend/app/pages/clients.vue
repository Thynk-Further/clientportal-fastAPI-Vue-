<template>
  <div class="max-w-6xl mx-auto space-y-6">
    
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Clients</h1>
        <p class="mt-1 text-sm text-gray-500">Manage your clients and their portal access.</p>
      </div>
      <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shrink-0">
        <Plus class="w-5 h-5 mr-1.5" />
        Add Client
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 3" :key="i" class="bg-white rounded-2xl border border-gray-100 p-6 h-32 animate-pulse">
        <div class="flex items-center gap-4 mb-4">
          <div class="w-12 h-12 bg-gray-200 rounded-full"></div>
          <div class="space-y-2 flex-1">
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            <div class="h-3 bg-gray-100 rounded w-3/4"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="clients.length === 0" class="bg-white rounded-3xl border border-dashed border-gray-300 p-12 text-center">
      <div class="w-16 h-16 bg-indigo-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <Users class="w-8 h-8 text-indigo-600" />
      </div>
      <h3 class="text-lg font-bold text-gray-900 mb-2">No clients found</h3>
      <p class="text-gray-500 max-w-sm mx-auto mb-6">You haven't added any clients yet. Add your first client to start collaborating.</p>
      <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">
        <Plus class="w-4 h-4 mr-2" />
        Add Client
      </button>
    </div>

    <!-- Clients Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="client in clients" :key="client.id" class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-all relative group">
        
        <!-- Options Dropdown using a simple relative div on hover (for MVP simplicity) -->
        <div class="absolute top-4 right-4 z-10">
          <div class="relative inline-block text-left group/dropdown">
            <button type="button" class="flex items-center text-gray-400 hover:text-gray-600 focus:outline-none" aria-haspopup="true">
              <MoreVertical class="w-5 h-5" />
            </button>
            <div class="origin-top-right absolute right-0 mt-2 w-56 rounded-xl shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 invisible opacity-0 group-hover/dropdown:visible group-hover/dropdown:opacity-100 transition-all focus:outline-none">
              <div class="py-1">
                <button @click="copyPortalLink(client.id)" class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 w-full text-left">
                  <Copy class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" />
                  Copy Portal Link
                </button>
              </div>
              <div class="py-1">
                <button @click="resendMagicLink(client.id)" :disabled="resendingId === client.id" class="group flex items-center px-4 py-2 text-sm text-indigo-700 hover:bg-indigo-50 w-full text-left disabled:opacity-50">
                  <RefreshCw v-if="resendingId === client.id" class="mr-3 h-4 w-4 text-indigo-400 animate-spin" />
                  <Mail v-else class="mr-3 h-4 w-4 text-indigo-400 group-hover:text-indigo-500" />
                  {{ resendingId === client.id ? 'Sending...' : 'Resend Magic Link' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="flex items-start gap-4">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center shrink-0 border border-indigo-50">
            <span class="text-indigo-700 font-bold text-lg">{{ client.name.charAt(0).toUpperCase() }}</span>
          </div>
          <div class="flex-1 min-w-0 pr-8">
            <h3 class="text-lg font-bold text-gray-900 truncate">{{ client.name }}</h3>
            <p v-if="client.company_name" class="text-sm font-medium text-indigo-600 truncate mb-1">{{ client.company_name }}</p>
            <div class="flex items-center text-sm text-gray-500">
              <Mail class="w-3.5 h-3.5 mr-1.5 shrink-0" />
              <span class="truncate">{{ client.email }}</span>
            </div>
          </div>
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-50 flex items-center justify-between">
          <span class="text-xs text-gray-400 font-medium">Added {{ new Date(client.created_at).toLocaleDateString() }}</span>
          <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-50 text-green-700 border border-green-100">
            Active
          </span>
        </div>
      </div>
    </div>

    <!-- The Add Client Modal Component -->
    <AddClientModal :is-open="isModalOpen" @close="isModalOpen = false" @client-added="handleClientAdded" />
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Users, MoreVertical, Copy, Mail, RefreshCw } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'
import AddClientModal from '~/components/AddClientModal.vue'

const api = useApi()

const clients = ref([])
const isLoading = ref(true)
const isModalOpen = ref(false)
const resendingId = ref(null)

const fetchClients = async () => {
  try {
    const data = await api('/api/v1/clients')
    clients.value = data
  } catch (err) {
    console.error('Failed to fetch clients', err)
  } finally {
    isLoading.value = false
  }
}

const handleClientAdded = (newClient) => {
  // Push the newly created client into the list so we don't have to refetch
  clients.value.unshift(newClient)
}

const copyPortalLink = async (clientId) => {
  try {
    // We only get the portal_token from the Detail endpoint!
    const clientDetail = await api(`/api/v1/clients/${clientId}`)
    const portalUrl = `${window.location.origin}/portal/${clientDetail.portal_token}`
    
    // Copy to clipboard
    await navigator.clipboard.writeText(portalUrl)
    alert('Portal link copied to clipboard!')
  } catch (err) {
    console.error('Failed to fetch portal link', err)
    alert('Failed to copy link.')
  }
}

const resendMagicLink = async (clientId) => {
  if (!confirm('This will invalidate their old portal link immediately and send them a new one. Are you sure?')) {
    return
  }

  resendingId.value = clientId
  try {
    await api(`/api/v1/clients/${clientId}/resend-link`, { method: 'POST' })
    alert('New magic link sent to the client via email!')
  } catch (err) {
    console.error('Failed to resend link', err)
    alert('Failed to resend link.')
  } finally {
    resendingId.value = null
  }
}

onMounted(() => {
  fetchClients()
})
</script>
