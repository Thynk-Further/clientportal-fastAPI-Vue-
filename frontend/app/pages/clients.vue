<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    <!-- Header with quick stats -->
    <section class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
          Workspace: Clients
        </h2>
        <p class="text-xs text-gray-400 mt-2">
          Manage corporate client accounts, explore billing configurations, and log onboarding times.
        </p>
      </div>
      <div class="flex gap-2">
        <button
          @click="showAddModal = true"
          class="bg-[#bef264] text-[#131f00] hover:bg-[#bef264]/80 font-bold px-5 py-3 rounded-lg text-sm transition-all duration-100 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider"
        >
          <span class="material-symbols-outlined text-md">person_add</span>
          Add Client
        </button>
      </div>
    </section>

    <!-- Corporate Grid Statistics -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-[#171717] border border-white/[0.08] p-5 rounded-xl flex items-center gap-4">
        <div class="bg-[#bef264]/10 text-[#bef264] p-3 rounded-xl shrink-0">
          <span class="material-symbols-outlined text-xl leading-none">handshake</span>
        </div>
        <div>
          <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider block">Connected Partners</span>
          <span class="text-2xl font-bold text-white leading-none mt-1 block">{{ clients.length }} Active</span>
        </div>
      </div>

      <div class="bg-[#171717] border border-white/[0.08] p-5 rounded-xl flex items-center gap-4">
        <div class="bg-[#bef264]/10 text-[#bef264] p-3 rounded-xl shrink-0">
          <span class="material-symbols-outlined text-xl leading-none">grade</span>
        </div>
        <div>
          <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider block">Avg Customer Rating</span>
          <span class="text-2xl font-bold text-white leading-none mt-1 block">4.9 ★★★★★</span>
        </div>
      </div>

      <div class="bg-[#171717] border border-white/[0.08] p-5 rounded-xl flex items-center gap-4">
        <div class="bg-[#bef264]/10 text-[#bef264] p-3 rounded-xl shrink-0">
          <span class="material-symbols-outlined text-xl leading-none">visibility</span>
        </div>
        <div>
          <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider block">Manager Workspace Link</span>
          <button
            @click="toggleRole"
            class="text-[#bef264] hover:underline text-xs font-bold font-mono mt-1 uppercase text-left tracking-wide block"
          >
            Simulate Client View →
          </button>
        </div>
      </div>
    </section>

    <!-- Filtering row -->
    <div class="py-2 border-y border-white/[0.05] bg-surface-container-lowest/20 flex flex-col md:flex-row gap-4 items-center justify-between">
      <span class="font-mono text-xs uppercase text-gray-400 tracking-wider">
        Querying Client Database: {{ filteredClients.length }} found
      </span>

      <div class="flex items-center gap-3 w-full md:w-auto">
        <!-- View Toggle -->
        <div class="flex items-center bg-[#1e2020] rounded-lg p-1 border border-white/5 shrink-0">
          <button @click="viewMode = 'grid'" :class="`p-1.5 rounded-md flex items-center justify-center transition-colors ${viewMode === 'grid' ? 'bg-[#2a2c2c] text-[#bef264]' : 'text-gray-500 hover:text-white'}`" title="Grid View">
            <span class="material-symbols-outlined text-sm">grid_view</span>
          </button>
          <button @click="viewMode = 'list'" :class="`p-1.5 rounded-md flex items-center justify-center transition-colors ${viewMode === 'list' ? 'bg-[#2a2c2c] text-[#bef264]' : 'text-gray-500 hover:text-white'}`" title="List View">
            <span class="material-symbols-outlined text-sm">format_list_bulleted</span>
          </button>
        </div>

        <div class="relative flex-1 md:w-[320px]">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400/40 text-lg select-none">
            search
          </span>
          <input
            v-model="search"
            type="text"
            placeholder="Search by name, company or email..."
            class="bg-[#1e2020] text-white rounded-lg pl-10 pr-4 py-2 w-full text-xs placeholder:text-gray-400/40 focus:outline-none focus:ring-1 focus:ring-[#bef264] transition-all"
          />
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 3" :key="i" class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden flex flex-col h-48 animate-pulse">
        <div class="h-2 bg-gradient-to-r from-gray-700 to-transparent"></div>
        <div class="p-6 flex-1 space-y-6"></div>
      </div>
    </div>

    <template v-else>
      <!-- Grid of clients -->
      <div v-if="filteredClients.length === 0" class="text-center py-20 bg-[#171717] border border-white/[0.08] rounded-xl">
        <span class="material-symbols-outlined text-4xl text-gray-400/40 mb-3 animate-pulse">
          groups
        </span>
        <p class="text-gray-400 font-mono text-xs">No client connections match your search query.</p>
      </div>

      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div
          v-for="(client, index) in filteredClients"
          :key="client.id"
          class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden flex flex-col hover:border-[#bef264]/20 transition-all duration-200 group"
        >
          <!-- Visual Header Grid Accent -->
          <div class="h-1 bg-gradient-to-r from-[#bef264]/20 to-transparent"></div>

          <div class="p-6 flex-1 space-y-6">
            <!-- Persona Bio -->
            <div class="flex items-center gap-4">
              <div :class="`w-10 h-10 rounded-full font-display font-semibold flex items-center justify-center text-sm shrink-0 ${
                index % 3 === 0
                  ? 'bg-gradient-to-br from-[#bef264] to-[#a3d64c] text-neutral-900 font-extrabold' 
                  : index % 3 === 1
                  ? 'bg-gradient-to-br from-blue-400 to-blue-600 text-white' 
                  : 'bg-gradient-to-br from-purple-400 to-purple-600 text-white'
              }`">
                {{ getInitials(client.name) }}
              </div>
              <div class="min-w-0 font-sans">
                <h4 class="font-bold text-white group-hover:text-[#bef264] transition-colors truncate">
                  {{ client.name }}
                </h4>
                <p class="text-[10px] text-gray-400 font-mono uppercase tracking-wider truncate">
                  {{ client.company_name || 'Independent' }}
                </p>
              </div>
            </div>

            <!-- Operational Metrics -->
            <div class="space-y-3.5 bg-white/[0.01] p-4 rounded-lg border border-white/[0.03] text-xs font-mono">
              <div class="flex justify-between items-center">
                <span class="text-gray-400 uppercase tracking-wider text-[10px]">Onboarding:</span>
                <span class="text-white font-medium text-[11px]">{{ new Date(client.created_at).toLocaleDateString() }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-400 uppercase tracking-wider text-[10px]">Active Sprints:</span>
                <span class="text-[#bef264] font-semibold text-[11px]">
                  {{ client.projectsCount || 0 }} {{ client.projectsCount === 1 ? 'Project' : 'Projects' }}
                </span>
              </div>
              <div class="flex flex-col gap-1 pt-2 border-t border-white/5">
                <span class="text-gray-400 uppercase tracking-wider block text-[10px]">Contact Node:</span>
                <span class="text-white truncate select-all text-[11px]">{{ client.email }}</span>
              </div>
            </div>
          </div>

          <!-- Simulation Action Bottom Bar -->
          <div class="border-t border-white/5 px-6 py-4 bg-[#1e2020]/30 flex items-center gap-3">
            <button
              @click="copyPortalLink(client.id)"
              class="flex-1 py-2 rounded-md text-[10px] font-bold font-mono uppercase tracking-wider bg-[#1e2020] hover:bg-[#bef264] hover:text-[#131f00] text-gray-400 hover:border-[#bef264] transition-all flex items-center justify-center gap-1.5 cursor-pointer border border-white/5"
            >
              <span class="material-symbols-outlined text-[14px]">content_copy</span>
              Copy Link
            </button>
            <button
              @click="openEditModal(client)"
              class="flex-1 py-2 rounded-md text-[10px] font-bold font-mono uppercase tracking-wider bg-[#1e2020] hover:bg-[#bef264] hover:text-[#131f00] text-gray-400 hover:border-[#bef264] transition-all flex items-center justify-center gap-1.5 cursor-pointer border border-white/5"
            >
              <span class="material-symbols-outlined text-[14px]">edit</span>
              Edit
            </button>
            <button
              @click="resendMagicLink(client.id)"
              :disabled="resendingId === client.id"
              class="flex-1 py-2 rounded-md text-[10px] font-bold font-mono uppercase tracking-wider bg-[#1e2020] hover:bg-[#bef264] hover:text-[#131f00] text-gray-400 hover:border-[#bef264] transition-all flex items-center justify-center gap-1.5 cursor-pointer border border-white/5 disabled:opacity-50"
            >
              <span v-if="resendingId === client.id" class="material-symbols-outlined animate-spin text-[14px]">progress_activity</span>
              <span v-else class="material-symbols-outlined text-[14px]">mark_email_unread</span>
              {{ resendingId === client.id ? 'Sending...' : 'Resend Link' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- List View -->
      <div v-else class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm whitespace-nowrap">
            <thead class="bg-white/[0.02] border-b border-white/[0.05] font-mono text-[10px] uppercase tracking-wider text-gray-400">
              <tr>
                <th class="px-6 py-4">Client Partner</th>
                <th class="px-6 py-4">Contact Node</th>
                <th class="px-6 py-4">Active Sprints</th>
                <th class="px-6 py-4">Onboarding</th>
                <th class="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/[0.05]">
              <tr v-for="(client, index) in filteredClients" :key="client.id" class="hover:bg-white/[0.01] transition-colors group">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div :class="`w-8 h-8 rounded-full font-display font-semibold flex items-center justify-center text-xs shrink-0 ${
                      index % 3 === 0
                        ? 'bg-gradient-to-br from-[#bef264] to-[#a3d64c] text-neutral-900 font-extrabold' 
                        : index % 3 === 1
                        ? 'bg-gradient-to-br from-blue-400 to-blue-600 text-white' 
                        : 'bg-gradient-to-br from-purple-400 to-purple-600 text-white'
                    }`">
                      {{ getInitials(client.name) }}
                    </div>
                    <div>
                      <div class="font-bold text-white group-hover:text-[#bef264] transition-colors">{{ client.name }}</div>
                      <div class="text-[10px] text-gray-400 font-mono uppercase">{{ client.company_name || 'Independent' }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-gray-300 font-mono text-[11px]">{{ client.email }}</td>
                <td class="px-6 py-4 text-[#bef264] font-semibold text-[11px] font-mono">
                  {{ client.projectsCount || 0 }} {{ client.projectsCount === 1 ? 'Project' : 'Projects' }}
                </td>
                <td class="px-6 py-4 text-gray-400 font-mono text-[11px]">
                  {{ new Date(client.created_at).toLocaleDateString() }}
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button @click="openEditModal(client)" class="p-2 bg-[#212323] hover:bg-[#bef264] hover:text-[#131f00] text-gray-400 hover:border-[#bef264] rounded-md transition-colors border border-white/5" title="Edit Client">
                      <span class="material-symbols-outlined text-[14px]">edit</span>
                    </button>
                    <button @click="copyPortalLink(client.id)" class="p-2 bg-[#212323] hover:bg-[#bef264] hover:text-[#131f00] text-gray-400 hover:border-[#bef264] rounded-md transition-colors border border-white/5" title="Copy Link">
                      <span class="material-symbols-outlined text-[14px]">content_copy</span>
                    </button>
                    <button @click="resendMagicLink(client.id)" :disabled="resendingId === client.id" class="p-2 bg-[#212323] hover:bg-[#bef264] hover:text-[#131f00] text-gray-400 hover:border-[#bef264] rounded-md transition-colors border border-white/5 disabled:opacity-50" title="Resend Link">
                      <span v-if="resendingId === client.id" class="material-symbols-outlined animate-spin text-[14px]">progress_activity</span>
                      <span v-else class="material-symbols-outlined text-[14px]">mark_email_unread</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- CREATE CLIENT DIALOG MODAL -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-8 max-w-md w-full space-y-6">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-xl font-bold text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-[#bef264]">person_add</span>
            Onboard New Client
          </h4>
          <button
            @click="showAddModal = false"
            class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer transition-colors"
          >
            close
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4 font-sans text-sm">
          <div v-if="submitError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
            {{ submitError }}
          </div>
          
          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Full Name</label>
            <input
              v-model="name"
              type="text"
              required
              placeholder="e.g. Sarah Jenkins"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Company / Venture</label>
            <input
              v-model="company"
              type="text"
              placeholder="e.g. Elysian Branding Group"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Email Node</label>
            <input
              v-model="email"
              type="email"
              required
              placeholder="e.g. sarah@elysian.com"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Phone Number</label>
            <input
              v-model="phone"
              type="text"
              placeholder="e.g. +1 555-0100"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Address</label>
            <input
              v-model="address"
              type="text"
              placeholder="e.g. 123 Business Rd, Suite 100"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="flex justify-end gap-2 text-sm pt-4">
            <button
              type="button"
              @click="showAddModal = false"
              :disabled="isSubmitting"
              class="px-5 py-2.5 rounded-lg hover:bg-white/[0.05] transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="px-6 py-2.5 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg cursor-pointer transform active:scale-95 transition-all text-xs uppercase font-mono tracking-wider disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="isSubmitting" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              Onboard Partner
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- EDIT CLIENT DIALOG MODAL -->
    <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-8 max-w-md w-full space-y-6">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-xl font-bold text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-[#bef264]">edit</span>
            Edit Client Profile
          </h4>
          <button
            @click="closeEditModal"
            class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer transition-colors"
          >
            close
          </button>
        </div>

        <form @submit.prevent="handleEditSubmit" class="space-y-4 font-sans text-sm">
          <div v-if="submitError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
            {{ submitError }}
          </div>
          
          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Full Name</label>
            <input
              v-model="editName"
              type="text"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Company / Venture</label>
            <input
              v-model="editCompany"
              type="text"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Email Node</label>
            <input
              v-model="editEmail"
              type="email"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Phone Number</label>
            <input
              v-model="editPhone"
              type="text"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Address</label>
            <input
              v-model="editAddress"
              type="text"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="flex justify-end gap-2 text-sm pt-4">
            <button
              type="button"
              @click="closeEditModal"
              :disabled="isSubmitting"
              class="px-5 py-2.5 rounded-lg hover:bg-white/[0.05] transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="px-6 py-2.5 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg cursor-pointer transform active:scale-95 transition-all text-xs uppercase font-mono tracking-wider disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="isSubmitting" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

const api = useApi()

const clients = ref([])
const isLoading = ref(true)
const search = ref('')
const viewMode = ref('grid') // 'grid' or 'list'
const showAddModal = ref(false)
const resendingId = ref(null)

// Edit Modal
const showEditModal = ref(false)
const editingClient = ref(null)

// Form states
const name = ref('')
const company = ref('')
const email = ref('')
const phone = ref('')
const address = ref('')
const isSubmitting = ref(false)
const submitError = ref('')

// Edit Form states
const editName = ref('')
const editCompany = ref('')
const editEmail = ref('')
const editPhone = ref('')
const editAddress = ref('')

const filteredClients = computed(() => {
  return clients.value.filter((client) => {
    return (
      client.name.toLowerCase().includes(search.value.toLowerCase()) ||
      (client.company_name && client.company_name.toLowerCase().includes(search.value.toLowerCase())) ||
      client.email.toLowerCase().includes(search.value.toLowerCase())
    )
  })
})

const fetchClients = async () => {
  try {
    const [clientsData, projectsData] = await Promise.all([
      api('/api/v1/clients'),
      api('/api/v1/projects')
    ])
    
    const projectCounts = {}
    if (projectsData) {
      projectsData.forEach(p => {
        projectCounts[p.client_id] = (projectCounts[p.client_id] || 0) + 1
      })
    }
    
    clients.value = clientsData.map(c => ({
      ...c, 
      projectsCount: projectCounts[c.id] || 0
    }))
  } catch (err) {
    console.error('Failed to fetch clients', err)
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  submitError.value = ''
  isSubmitting.value = true
  try {
    const newClient = await api('/api/v1/clients', {
      method: 'POST',
      body: {
        name: name.value,
        company_name: company.value || null,
        email: email.value,
        phone: phone.value || null,
        address: address.value || null
      }
    })
    
    clients.value.unshift({...newClient, projectsCount: 0})
    
    // Reset states
    name.value = ''
    company.value = ''
    email.value = ''
    phone.value = ''
    address.value = ''
    showAddModal.value = false
  } catch (err) {
    submitError.value = err.message || 'Failed to add client.'
  } finally {
    isSubmitting.value = false
  }
}

const openEditModal = (client) => {
  editingClient.value = client
  editName.value = client.name
  editEmail.value = client.email
  editCompany.value = client.company_name || ''
  editPhone.value = client.phone || ''
  editAddress.value = client.address || ''
  submitError.value = ''
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingClient.value = null
}

const handleEditSubmit = async () => {
  submitError.value = ''
  isSubmitting.value = true
  try {
    const updatedClient = await api(`/api/v1/clients/${editingClient.value.id}`, {
      method: 'PATCH',
      body: {
        name: editName.value,
        email: editEmail.value,
        company_name: editCompany.value || null,
        phone: editPhone.value || null,
        address: editAddress.value || null
      }
    })

    const idx = clients.value.findIndex(c => c.id === updatedClient.id)
    if (idx !== -1) {
      clients.value[idx] = { ...clients.value[idx], ...updatedClient }
    }

    closeEditModal()
  } catch (err) {
    submitError.value = err.data?.detail || 'Failed to update client.'
  } finally {
    isSubmitting.value = false
  }
}

const getInitials = (n) => {
  if (!n) return '?'
  return n.split(' ').map((p) => p[0]).join('').slice(0, 2).toUpperCase()
}

const toggleRole = () => {
  alert("Roles Swapped! You are currently exploring the app as a client partner. Click 'Switch role' button at the bottom of the sidebar at any time to return to manager view.")
}

const copyPortalLink = async (clientId) => {
  try {
    const clientDetail = await api(`/api/v1/clients/${clientId}`)
    const portalUrl = `${window.location.origin}/portal/${clientDetail.portal_token}`
    
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
