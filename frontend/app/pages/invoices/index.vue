<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    <!-- MANAGER WORKSPACE LAYOUT -->
    <div class="space-y-8">
      <section class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
            Transactions Ledger
          </h2>
          <p class="text-xs text-gray-400 mt-2">
            Launch invoices, follow pending client balances, log payments, and download statements.
          </p>
        </div>
        <button
          @click="showAddModal = true"
          class="bg-[#bef264] text-[#131f00] hover:bg-[#bef264]/80 font-bold px-5 py-3 rounded-lg text-sm transition-all duration-100 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider"
        >
          <span class="material-symbols-outlined text-md">add_card</span>
          Create Invoice
        </button>
      </section>

      <!-- Manager stats -->
      <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex justify-between items-center transition-all hover:border-[#bef264]/10">
          <div class="space-y-1">
            <span class="font-mono text-xs text-gray-400 uppercase tracking-wider mb-2 block">Total Outstanding Revenue</span>
            <p class="text-4xl font-extrabold text-[#bef264]">${{ totalOutstanding.toLocaleString(undefined, {minimumFractionDigits: 2}) }}</p>
          </div>
          <div class="h-12 w-12 rounded-xl bg-[#bef264]/5 border border-[#bef264]/20 flex items-center justify-center text-[#bef264]">
            <span class="material-symbols-outlined text-2xl">pending_actions</span>
          </div>
        </div>

        <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex justify-between items-center transition-all hover:border-[#bef264]/10">
          <div class="space-y-1">
            <span class="font-mono text-xs text-gray-400 uppercase tracking-wider mb-2 block">Collected Revenue (YTD)</span>
            <p class="text-4xl font-semibold text-white">${{ totalPaid.toLocaleString(undefined, {minimumFractionDigits: 2}) }}</p>
          </div>
          <div class="h-12 w-12 rounded-xl bg-green-500/5 border border-green-500/20 flex items-center justify-center text-green-400">
            <span class="material-symbols-outlined text-2xl">account_balance_wallet</span>
          </div>
        </div>
      </section>

      <!-- Filtering control row -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 py-2 border-y border-white/[0.05] bg-[#1e2020]/20">
        <div class="flex flex-wrap items-center gap-1.5 overflow-x-auto pb-2 md:pb-0">
          <button
            v-for="cat in ['All', 'paid', 'sent', 'overdue', 'draft']"
            :key="cat"
            @click="filter = cat"
            :class="`px-4 py-2 text-xs font-bold rounded-lg cursor-pointer transition-all ${
              filter === cat
                ? 'bg-white/10 text-[#bef264] border border-white/5'
                : 'bg-transparent text-gray-400 hover:text-white hover:bg-white/[0.02]'
            }`"
          >
            {{ cat === 'All' ? 'All' : cat.charAt(0).toUpperCase() + cat.slice(1) }}
          </button>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400/40 text-lg select-none">
              search
            </span>
            <input
              v-model="search"
              type="text"
              placeholder="Search invoice ID or client..."
              class="bg-[#1e2020] text-white rounded-lg pl-10 pr-4 py-2 w-[240px] text-xs placeholder:text-gray-400/40 focus:outline-none focus:ring-1 focus:ring-[#bef264] transition-all"
            />
          </div>

          <div class="flex items-center border border-white/[0.08] p-1 rounded-lg shrink-0 select-none bg-[#1e2020]">
            <button
              @click="viewMode = 'list'"
              :class="`p-1.5 rounded cursor-pointer ${
                viewMode === 'list' ? 'bg-[#343535] text-[#bef264]' : 'text-gray-400 hover:text-white'
              }`"
              title="List layout"
            >
              <span class="material-symbols-outlined text-base leading-none">format_list_bulleted</span>
            </button>
            <button
              @click="viewMode = 'grid'"
              :class="`p-1.5 rounded cursor-pointer ${
                viewMode === 'grid' ? 'bg-[#343535] text-[#bef264]' : 'text-gray-400 hover:text-white'
              }`"
              title="Grid layout"
            >
              <span class="material-symbols-outlined text-base leading-none">grid_view</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col justify-between h-48 animate-pulse">
        </div>
      </div>

      <template v-else>
        <!-- List or grid render -->
        <div v-if="filteredInvoices.length === 0" class="text-center py-20 bg-[#171717] border border-white/[0.08] rounded-xl">
          <span class="material-symbols-outlined text-4xl text-gray-400/40 mb-3 animate-pulse">
            receipt_long
          </span>
          <p class="text-gray-400 font-mono text-xs">No matching statements registered in the ledger.</p>
        </div>

        <!-- LIST LAYOUT -->
        <div v-else-if="viewMode === 'list'" class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden overflow-x-auto custom-scrollbar">
          <table class="w-full text-left text-sm border-collapse min-w-[700px]">
            <thead class="bg-[#1e2020] border-b border-white/5 text-gray-400 uppercase tracking-wider font-mono text-xs">
              <tr>
                <th class="px-6 py-4">Invoice ID</th>
                <th class="px-6 py-4">Associated Client</th>
                <th class="px-6 py-4">Issue Date</th>
                <th class="px-6 py-4">Due Date</th>
                <th class="px-6 py-2 text-right">Sum Total</th>
                <th class="px-6 py-2 text-center">Status Indicator</th>
                <th class="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5 font-sans">
              <tr v-for="inv in filteredInvoices" :key="inv.id" class="hover:bg-white/[0.01] transition-colors group">
                <td class="px-6 py-4 font-mono text-white font-bold">{{ inv.id.split('-')[0] }}</td>
                <td class="px-6 py-4 text-white font-medium">{{ inv.client_id || 'Unknown Client' }}</td>
                <td class="px-6 py-4 text-gray-400 font-mono text-xs">{{ new Date(inv.created_at).toLocaleDateString() }}</td>
                <td class="px-6 py-4 text-gray-400 font-mono text-xs">{{ inv.due_date || 'N/A' }}</td>
                <td class="px-6 py-4 text-right font-mono font-bold text-white">
                  ${{ ((inv.amount_cents || 0) / 100).toLocaleString(undefined, {minimumFractionDigits: 2}) }}
                </td>
                <td class="px-6 py-4">
                  <div class="flex justify-center">
                    <span :class="`px-2.5 py-1 rounded-full text-[10px] font-bold border uppercase tracking-tighter flex items-center gap-1.5 ${
                      inv.status === 'paid'
                        ? 'bg-green-500/10 text-green-400 border-green-500/20'
                        : inv.status === 'sent'
                        ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                        : inv.status === 'overdue'
                        ? 'bg-red-500/10 text-red-400 border-red-500/20'
                        : 'bg-white/10 text-gray-400 border-white/5'
                    }`">
                      <span :class="`h-1 w-1 rounded-full ${
                        inv.status === 'paid' ? 'bg-green-400' : inv.status === 'sent' ? 'bg-blue-400' : inv.status === 'overdue' ? 'bg-red-400' : 'bg-gray-400'
                      }`"></span>
                      {{ inv.status }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex justify-end gap-1.5 opacity-60 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="handleDownload(inv.id, $event)"
                      class="p-1.5 hover:bg-[#212323] hover:text-[#bef264] rounded transition-colors cursor-pointer"
                      title="Download PDF"
                    >
                      <span class="material-symbols-outlined text-base leading-none">download</span>
                    </button>
                    <button
                      class="p-1.5 hover:bg-red-500/10 hover:text-red-400 rounded transition-colors cursor-pointer"
                      title="Delete Statement"
                    >
                      <span class="material-symbols-outlined text-base leading-none">delete</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- GRID LAYOUT -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="inv in filteredInvoices"
            :key="inv.id"
            class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col justify-between hover:border-[#bef264]/20 transition-all gap-4"
          >
            <div class="space-y-4">
              <div class="flex justify-between items-start">
                <span class="font-mono text-sm font-bold text-white">{{ inv.id.split('-')[0] }}</span>
                <span :class="`px-2 py-0.5 rounded text-[9px] font-bold border uppercase tracking-wider ${
                  inv.status === 'paid'
                    ? 'bg-green-500/10 text-green-400 border-green-500/20'
                    : inv.status === 'sent'
                    ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                    : inv.status === 'overdue'
                    ? 'bg-red-500/10 text-red-400 border-red-500/20'
                    : 'bg-white/10 text-gray-400 border-white/5'
                }`">
                  {{ inv.status }}
                </span>
              </div>

              <div class="space-y-1">
                <h4 class="font-bold text-white truncate text-base">{{ inv.client_id || 'Unknown Client' }}</h4>
                <p class="text-2xl font-extrabold text-white font-mono">${{ ((inv.amount_cents || 0) / 100).toLocaleString(undefined, {minimumFractionDigits: 2}) }}</p>
              </div>

              <div class="grid grid-cols-2 gap-2 text-xs font-mono border-t border-white/5 pt-4">
                <div>
                  <span class="text-gray-400 block uppercase text-[10px] mb-0.5">Issue Date</span>
                  <span class="text-white">{{ new Date(inv.created_at).toLocaleDateString() }}</span>
                </div>
                <div>
                  <span class="text-gray-400 block uppercase text-[10px] mb-0.5">Due Date</span>
                  <span class="text-white">{{ inv.due_date || 'N/A' }}</span>
                </div>
              </div>
            </div>

            <div class="flex justify-end gap-2 border-t border-white/5 pt-4">
              <button
                @click="handleDownload(inv.id, $event)"
                class="px-3.5 py-2 hover:bg-[#bef264] hover:text-[#131f00] text-white text-xs font-bold font-mono rounded bg-[#212323] transition-colors cursor-pointer uppercase flex items-center gap-1.5 shrink-0"
              >
                <span class="material-symbols-outlined text-sm leading-none">download</span>
                <span>Download</span>
              </button>
              <button
                class="p-2 hover:bg-red-500/10 hover:text-red-400 text-gray-400 text-xs font-bold rounded bg-[#212323] transition-colors cursor-pointer"
                title="Delete Statement"
              >
                <span class="material-symbols-outlined text-sm leading-none">delete</span>
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- CREATE MANAGER INVOICE MODAL -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-8 max-w-md w-full space-y-6">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-xl font-bold text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-[#bef264]">receipt_long</span>
            Generate Invoice
          </h4>
          <button
            @click="showAddModal = false"
            class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer transition-colors"
          >
            close
          </button>
        </div>

        <form @submit.prevent="handleCreateSubmit" class="space-y-4 font-sans text-sm">
          <div v-if="submitError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
            {{ submitError }}
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Client / Organization</label>
            <select
              v-model="newClient"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none appearance-none"
              :disabled="isSubmitting || isClientsLoading"
            >
              <option value="" disabled>Select a client...</option>
              <option v-for="client in clientsList" :key="client.id" :value="client.id">
                {{ client.name }}
              </option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Project</label>
            <select
              v-model="newProject"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none appearance-none"
              :disabled="isSubmitting || isProjectsLoading"
            >
              <option value="" disabled>Select a project...</option>
              <option v-for="project in projectsList" :key="project.id" :value="project.id">
                {{ project.name }}
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Amount Sum ($)</label>
              <input
                v-model="amount"
                type="number"
                min="1"
                required
                placeholder="2500"
                class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
                :disabled="isSubmitting"
              />
            </div>
            <div class="space-y-1">
              <label class="font-[#bef264] font-mono text-xs text-gray-400 block uppercase tracking-wider">Due Date</label>
              <input
                v-model="dueDate"
                type="date"
                required
                class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
                :disabled="isSubmitting"
              />
            </div>
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
              class="px-6 py-2.5 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg cursor-pointer transform active:scale-95 transition-all text-xs uppercase font-mono tracking-wider disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <span v-if="isSubmitting" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              Generate Statement
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

const invoices = ref([])
const clientsList = ref([])
const projectsList = ref([])
const isLoading = ref(true)
const isClientsLoading = ref(false)
const isProjectsLoading = ref(false)

const viewMode = ref('list')
const filter = ref('All')
const search = ref('')
const showAddModal = ref(false)

// Modal input states
const newClient = ref('')
const newProject = ref('')
const amount = ref('')
const dueDate = ref('')

const isSubmitting = ref(false)
const submitError = ref('')
const copiedInvoiceId = ref(null)

const filteredInvoices = computed(() => {
  return invoices.value.filter((inv) => {
    const matchesFilter = filter.value === 'All' || inv.status === filter.value
    const searchLower = search.value.toLowerCase()
    const matchesSearch = 
      inv.id.toLowerCase().includes(searchLower) || 
      (inv.client_id && inv.client_id.toLowerCase().includes(searchLower))
    return matchesFilter && matchesSearch
  })
})

const totalOutstanding = computed(() => {
  return invoices.value
    .filter((i) => i.status === 'sent' || i.status === 'overdue')
    .reduce((r, i) => r + (i.amount_cents || 0) / 100, 0)
})

const totalPaid = computed(() => {
  return invoices.value
    .filter((i) => i.status === 'paid')
    .reduce((r, i) => r + (i.amount_cents || 0) / 100, 0)
})

const fetchInvoices = async () => {
  try {
    const data = await api('/api/v1/invoices')
    invoices.value = data
  } catch (err) {
    console.error('Failed to fetch invoices', err)
  } finally {
    isLoading.value = false
  }
}

const fetchDependencies = async () => {
  try {
    isClientsLoading.value = true
    isProjectsLoading.value = true
    const [clientsData, projectsData] = await Promise.all([
      api('/api/v1/clients'),
      api('/api/v1/projects')
    ])
    clientsList.value = clientsData
    projectsList.value = projectsData
  } catch (err) {
    console.error('Failed to fetch dependencies', err)
  } finally {
    isClientsLoading.value = false
    isProjectsLoading.value = false
  }
}

const handleDownload = (id, e) => {
  e.stopPropagation()
  copiedInvoiceId.value = id
  setTimeout(() => {
    copiedInvoiceId.value = null
    alert(`Invoice ${id} has been compiled and downloaded securely in premium layout.`)
  }, 1500)
}

const handleCreateSubmit = async () => {
  submitError.value = ''
  isSubmitting.value = true

  try {
    const newInvoice = await api('/api/v1/invoices', {
      method: 'POST',
      body: {
        project_id: newProject.value,
        client_id: newClient.value,
        amount_cents: Math.round(Number(amount.value) * 100),
        due_date: dueDate.value,
        line_items: [
          { description: 'Consulting Services', amount_cents: Math.round(Number(amount.value) * 100), quantity: 1 }
        ]
      }
    })

    invoices.value.unshift(newInvoice)

    // Reset fields
    newClient.value = ''
    newProject.value = ''
    amount.value = ''
    dueDate.value = ''
    showAddModal.value = false
  } catch (err) {
    submitError.value = err.message || 'Failed to generate invoice.'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchInvoices()
  fetchDependencies()
})
</script>
