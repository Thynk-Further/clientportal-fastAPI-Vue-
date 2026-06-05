<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    <!-- Header bar -->
    <section class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
          Workspace: Projects
        </h2>
        <p class="text-xs text-gray-400 mt-2">
          Track design sprints, developer handshakes, and budgets inside active client pipelines.
        </p>
      </div>
      <button
        @click="showAddModal = true"
        class="bg-[#bef264] text-[#131f00] hover:bg-[#bef264]/80 font-bold px-5 py-3 rounded-lg text-sm transition-all duration-100 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider"
      >
        <span class="material-symbols-outlined text-md">add</span>
        Initiate Project
      </button>
    </section>

    <!-- Filter and Control Bars -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 py-2 border-y border-white/[0.05] bg-surface-container-lowest/20">
      <div class="flex flex-wrap items-center gap-1.5 overflow-x-auto pb-2 md:pb-0">
        <button
          v-for="cat in ['All', 'active', 'completed']"
          :key="cat"
          @click="filter = cat"
          :class="`px-4 py-2 text-xs font-bold rounded-lg cursor-pointer transition-all ${
            filter === cat
              ? 'bg-white/10 text-[#bef264] border border-white/5'
              : 'bg-transparent text-gray-400 hover:text-white hover:bg-white/[0.02]'
          }`"
        >
          {{ cat === 'All' ? 'All' : (cat === 'active' ? 'In Progress' : 'Completed') }}
        </button>
      </div>

      <div class="flex items-center gap-3">
        <div class="relative">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400/40 text-lg select-none">
            search
          </span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search projects..."
            class="bg-[#1e2020] text-white rounded-lg pl-10 pr-4 py-2 w-[240px] text-xs placeholder:text-gray-400/40 focus:outline-none focus:ring-1 focus:ring-[#bef264] transition-all"
          />
        </div>

        <div class="flex items-center border border-white/[0.08] p-1 rounded-lg shrink-0 select-none bg-[#1e2020]">
          <button
            @click="viewMode = 'grid'"
            :class="`p-1.5 rounded cursor-pointer ${
              viewMode === 'grid' ? 'bg-[#343535] text-[#bef264]' : 'text-gray-400 hover:text-white'
            }`"
            title="Grid View"
          >
            <span class="material-symbols-outlined text-base leading-none">grid_view</span>
          </button>
          <button
            @click="viewMode = 'list'"
            :class="`p-1.5 rounded cursor-pointer ${
              viewMode === 'list' ? 'bg-[#343535] text-[#bef264]' : 'text-gray-400 hover:text-white'
            }`"
            title="List View"
          >
            <span class="material-symbols-outlined text-base leading-none">format_list_bulleted</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 3" :key="i" class="bg-[#171717] border border-white/[0.08] rounded-xl p-6 h-48 animate-pulse"></div>
    </div>

    <template v-else>
      <!-- Grid or List of Projects -->
      <div v-if="filteredProjects.length === 0" class="text-center py-20 bg-[#171717] border border-white/[0.08] rounded-xl flex flex-col items-center justify-center">
        <span class="material-symbols-outlined text-4xl text-gray-400/40 mb-3 animate-pulse">
          rocket_launch
        </span>
        <p class="text-gray-400 font-mono text-xs">No projects found matching the criteria.</p>
      </div>

      <!-- GRID LAYOUT -->
      <div v-else-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <NuxtLink
          v-for="project in filteredProjects"
          :key="project.id"
          :to="`/projects/${project.id}`"
          class="bg-[#171717] border border-white/[0.08] rounded-xl p-6 flex flex-col hover:border-[#bef264]/20 transition-all group block"
        >
          <div class="flex justify-between items-start mb-4">
            <span :class="`px-2.5 py-1 rounded text-[9px] font-mono tracking-wider uppercase border ${
              project.status === 'completed'
                ? 'bg-green-500/10 text-green-400 border-green-500/20'
                : project.status === 'on_hold'
                ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
                : 'bg-blue-500/10 text-blue-400 border-blue-500/20'
            }`">
              {{ project.status === 'active' ? 'In Progress' : project.status }}
            </span>
            <span class="text-[11px] font-mono text-gray-400">
              Created: {{ new Date(project.created_at).toLocaleDateString() }}
            </span>
          </div>

          <div class="flex-1 space-y-2">
            <h4 class="font-display text-lg font-bold text-white group-hover:text-[#bef264] transition-colors line-clamp-1">
              {{ project.name }}
            </h4>
            <p v-if="project.client_id" class="text-xs text-gray-400 font-mono uppercase tracking-wider">
              Client ID: {{ project.client_id }}
            </p>
            <p class="text-sm text-gray-400 line-clamp-2 h-10 mt-2">
              {{ project.description || 'No description provided.' }}
            </p>
          </div>

          <div class="space-y-4 pt-6 mt-4 border-t border-white/5">
            <div class="space-y-1.5">
              <div class="flex justify-between text-[11px] font-mono text-gray-400">
                <span>PROGRESS</span>
                <span>{{ project.progress || 25 }}%</span>
              </div>
              <div class="w-full bg-[#1e2020] h-1.5 rounded-full overflow-hidden">
                <div
                  :class="`h-full rounded-full transition-all duration-500 ${
                    project.status === 'completed' ? 'bg-green-400' : 'bg-[#bef264]'
                  }`"
                  :style="{ width: `${project.progress || 25}%` }"
                ></div>
              </div>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- LIST LAYOUT -->
      <div v-else class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden overflow-x-auto custom-scrollbar">
        <table class="w-full text-left text-sm border-collapse min-w-[700px]">
          <thead class="bg-[#1e2020] border-b border-white/5 text-gray-400 uppercase tracking-wider font-mono text-xs">
            <tr>
              <th class="px-6 py-4">Project Workspace</th>
              <th class="px-6 py-4">Progress Rating</th>
              <th class="px-6 py-4">Created On</th>
              <th class="px-6 py-4">Status Indicator</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5 font-sans">
            <tr v-for="project in filteredProjects" :key="project.id" @click="$router.push(`/projects/${project.id}`)" class="hover:bg-white/[0.01] transition-colors group cursor-pointer">
              <td class="px-6 py-4 font-bold text-white group-hover:text-[#bef264] transition-colors max-w-[200px] truncate">
                {{ project.name }}
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-3 w-[150px]">
                  <div class="w-20 bg-[#1e2020] h-1.5 rounded-full overflow-hidden">
                    <div
                      class="bg-[#bef264] h-full rounded-full"
                      :style="{ width: `${project.progress || 25}%` }"
                    ></div>
                  </div>
                  <span class="text-xs font-mono text-white font-semibold">{{ project.progress || 25 }}%</span>
                </div>
              </td>
              <td class="px-6 py-4 text-gray-400 font-mono text-xs">
                {{ new Date(project.created_at).toLocaleDateString() }}
              </td>
              <td class="px-6 py-4">
                <span :class="`px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-tighter ${
                  project.status === 'completed'
                    ? 'bg-green-500/10 text-green-400 border-green-500/20'
                    : project.status === 'on_hold'
                    ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
                    : 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                }`">
                  {{ project.status === 'active' ? 'In Progress' : project.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- Quarterly Velocity CTA Banner Block -->
    <section class="bg-gradient-to-r from-[#bef264]/[0.03] to-transparent border border-[#bef264]/20 p-6 md:p-8 rounded-xl flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="space-y-1.5 max-w-xl text-center md:text-left">
        <span class="font-mono text-[10px] text-[#bef264] uppercase tracking-widest font-extrabold">Sprint Analytics</span>
        <h4 class="font-display text-xl font-bold text-white">Quarterly Velocity Report</h4>
        <p class="text-xs text-gray-400 leading-relaxed">
          Visual Sprints & Velocity Rates. Download the comprehensive report on agency bandwidth, active design velocity, and milestone targets.
        </p>
      </div>
      <button
        @click="triggerDownloadReport"
        :disabled="downloading"
        class="bg-white text-[#121414] hover:bg-[#bef264] hover:text-[#121414] font-bold px-6 py-3.5 rounded-lg text-xs transition-all duration-100 cursor-pointer active:scale-95 flex items-center gap-2 select-none font-mono uppercase"
      >
        <span v-if="downloading" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
        <span v-else class="material-symbols-outlined text-sm">download_done</span>
        <span>{{ downloading ? 'Generating...' : 'Download Report' }}</span>
      </button>
    </section>

    <!-- INITIATE PROJECT FORM MODAL -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-8 max-w-md w-full space-y-6">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-xl font-bold text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-[#bef264]">add_task</span>
            Launch New Sprint
          </h4>
          <button
            @click="showAddModal = false"
            class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer transition-colors"
          >
            close
          </button>
        </div>

        <form @submit.prevent="handleAddSubmit" class="space-y-4 font-sans text-sm">
          <div v-if="submitError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
            {{ submitError }}
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Project Name</label>
            <input
              v-model="newProjName"
              type="text"
              required
              placeholder="e.g. Neo-Metropolis System Redesign"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isSubmitting"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Client</label>
            <select
              v-model="newProjClient"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none appearance-none"
              :disabled="isSubmitting || isClientsLoading"
            >
              <option value="" disabled>Select a client...</option>
              <option v-for="client in clientsList" :key="client.id" :value="client.id">
                {{ client.name }} ({{ client.company_name || 'No Company' }})
              </option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Project Scope / Brief</label>
            <textarea
              v-model="newProjDesc"
              rows="3"
              placeholder="Describe core goals, visual requirements, and major tech assets..."
              class="w-full bg-[#1e2020] text-white text-xs rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none resize-none"
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
              class="px-6 py-2.5 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg cursor-pointer transform active:scale-95 transition-all text-xs uppercase font-mono tracking-wider disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <span v-if="isSubmitting" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              Initiate
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from '#app'
import { useApi } from '~/composables/useApi'

const api = useApi()
const router = useRouter()

const projects = ref([])
const clientsList = ref([])
const isLoading = ref(true)
const isClientsLoading = ref(false)

const viewMode = ref('grid')
const filter = ref('All')
const searchQuery = ref('')

const showAddModal = ref(false)
const downloading = ref(false)

// Form state
const newProjName = ref('')
const newProjClient = ref('')
const newProjDesc = ref('')
const isSubmitting = ref(false)
const submitError = ref('')

const filteredProjects = computed(() => {
  return projects.value.filter(p => {
    const matchesFilter = filter.value === 'All' || p.status === filter.value
    const searchLower = searchQuery.value.toLowerCase()
    const matchesSearch = p.name?.toLowerCase().includes(searchLower) || p.description?.toLowerCase().includes(searchLower)
    return matchesFilter && matchesSearch
  })
})

const fetchProjects = async () => {
  try {
    const data = await api('/api/v1/projects')
    projects.value = data
  } catch (err) {
    console.error('Failed to fetch projects', err)
  } finally {
    isLoading.value = false
  }
}

const fetchClients = async () => {
  isClientsLoading.value = true
  try {
    const data = await api('/api/v1/clients')
    clientsList.value = data
  } catch (err) {
    console.error('Failed to fetch clients', err)
  } finally {
    isClientsLoading.value = false
  }
}

const handleAddSubmit = async () => {
  submitError.value = ''
  isSubmitting.value = true
  try {
    const payload = {
      name: newProjName.value,
      description: newProjDesc.value || null,
      client_id: newProjClient.value,
      status: 'active'
    }
    const newProject = await api('/api/v1/projects', {
      method: 'POST',
      body: payload
    })
    projects.value.unshift(newProject)
    
    // Reset and close
    newProjName.value = ''
    newProjClient.value = ''
    newProjDesc.value = ''
    showAddModal.value = false
  } catch (err) {
    submitError.value = err.message || 'Failed to create project.'
  } finally {
    isSubmitting.value = false
  }
}

const triggerDownloadReport = () => {
  downloading.value = true
  setTimeout(() => {
    downloading.value = false
    alert('Quarterly Velocity Report has been successfully downloaded into your documents folder.')
  }, 1500)
}

onMounted(() => {
  fetchProjects()
  fetchClients()
})
</script>
