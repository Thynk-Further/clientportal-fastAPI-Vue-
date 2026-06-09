<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    
    <!-- Welcome Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h2 class="font-display text-2xl font-bold text-white tracking-tight">
          Welcome back, {{ authStore.user?.full_name?.split(' ')[0] || 'User' }}
        </h2>
        <p class="text-sm text-gray-400 mt-1">Here is what's happening with your projects today.</p>
      </div>
      <div class="flex gap-3">
        <button class="bg-[#1e2020] text-white hover:bg-[#212323] px-4 py-2 rounded-lg font-bold flex items-center gap-2 border border-white/5 transition-colors text-sm">
          <span class="material-symbols-outlined text-[18px]">download</span>
          Download Report
        </button>
        <button class="bg-[#bef264] text-[#131f00] hover:bg-[#a3d64c] px-4 py-2 rounded-lg font-bold flex items-center gap-2 transition-colors text-sm">
          <span class="material-symbols-outlined text-[18px]">add</span>
          New Lead
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="animate-pulse space-y-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i" class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl h-32"></div>
      </div>
    </div>

    <template v-else>
      <!-- Top Stats Row -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Total Revenue -->
        <div class="bg-[#171717] border border-white/[0.08] p-5 rounded-xl flex flex-col justify-between group hover:border-[#bef264]/20 transition-all">
          <div class="flex justify-between items-start mb-4">
            <div class="bg-white/5 p-2 rounded-lg text-gray-300">
              <span class="material-symbols-outlined text-[20px]">payments</span>
            </div>
            <span class="text-[#bef264] text-xs font-bold flex items-center bg-[#bef264]/10 px-2 py-1 rounded-full">
              <span class="material-symbols-outlined text-[14px] mr-1">trending_up</span>
              +12.5%
            </span>
          </div>
          <div>
            <p class="text-xs text-gray-400 font-mono uppercase tracking-wider mb-1">Total Revenue</p>
            <h3 class="text-3xl font-extrabold text-white">$24,500<span class="text-lg text-gray-500 font-normal">.00</span></h3>
          </div>
        </div>

        <!-- Active Projects -->
        <div class="bg-[#171717] border border-white/[0.08] p-5 rounded-xl flex flex-col justify-between group hover:border-[#bef264]/20 transition-all">
          <div class="flex justify-between items-start mb-4">
            <div class="bg-white/5 p-2 rounded-lg text-gray-300">
              <span class="material-symbols-outlined text-[20px]">rocket_launch</span>
            </div>
            <span class="text-gray-400 text-xs font-bold flex items-center bg-white/5 px-2 py-1 rounded-full">
              Same as last month
            </span>
          </div>
          <div>
            <p class="text-xs text-gray-400 font-mono uppercase tracking-wider mb-1">Active Projects</p>
            <div class="flex items-baseline gap-2">
              <h3 class="text-3xl font-extrabold text-white">{{ projects.length }}</h3>
            </div>
          </div>
        </div>

        <!-- Pending Invoices -->
        <div class="bg-[#171717] border border-white/[0.08] p-5 rounded-xl flex flex-col justify-between group hover:border-[#bef264]/20 transition-all">
          <div class="flex justify-between items-start mb-4">
            <div class="bg-white/5 p-2 rounded-lg text-gray-300">
              <span class="material-symbols-outlined text-[20px]">receipt_long</span>
            </div>
            <span class="text-red-400 text-xs font-bold flex items-center bg-red-400/10 px-2 py-1 rounded-full">
              2 Overdue
            </span>
          </div>
          <div>
            <p class="text-xs text-gray-400 font-mono uppercase tracking-wider mb-1">Pending Invoices</p>
            <h3 class="text-3xl font-extrabold text-white">4</h3>
          </div>
        </div>

        <!-- New Leads -->
        <div class="bg-[#171717] border border-white/[0.08] p-5 rounded-xl flex flex-col justify-between group hover:border-[#bef264]/20 transition-all">
          <div class="flex justify-between items-start mb-4">
            <div class="bg-white/5 p-2 rounded-lg text-gray-300">
              <span class="material-symbols-outlined text-[20px]">group_add</span>
            </div>
            <span class="text-[#bef264] text-xs font-bold flex items-center bg-[#bef264]/10 px-2 py-1 rounded-full">
              <span class="material-symbols-outlined text-[14px] mr-1">trending_up</span>
              +5%
            </span>
          </div>
          <div>
            <p class="text-xs text-gray-400 font-mono uppercase tracking-wider mb-1">New Leads</p>
            <h3 class="text-3xl font-extrabold text-white">{{ clients.length }}</h3>
          </div>
        </div>

      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Left Column: Chart & Projects -->
        <div class="lg:col-span-2 space-y-8">
          
          <!-- Revenue Performance Chart -->
          <div class="bg-[#171717] border border-white/[0.08] rounded-xl p-6">
            <div class="flex justify-between items-center mb-6">
              <h3 class="font-display font-bold text-white text-lg">Revenue Performance</h3>
              <select class="bg-[#1e2020] text-xs text-gray-300 rounded border border-white/10 px-2 py-1 outline-none">
                <option>Last 6 Months</option>
                <option>This Year</option>
              </select>
            </div>
            <div class="h-64 w-full relative">
              <!-- Mock SVG Chart -->
              <svg viewBox="0 0 800 200" class="w-full h-full drop-shadow-lg" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#bef264" stop-opacity="0.3" />
                    <stop offset="100%" stop-color="#bef264" stop-opacity="0" />
                  </linearGradient>
                </defs>
                <path d="M0,180 C100,150 200,80 300,120 C400,160 500,40 600,90 C700,140 800,20 800,20 L800,200 L0,200 Z" fill="url(#gradient)" />
                <path d="M0,180 C100,150 200,80 300,120 C400,160 500,40 600,90 C700,140 800,20 800,20" fill="none" stroke="#bef264" stroke-width="3" stroke-linecap="round" class="drop-shadow-md" />
                
                <!-- Data Points -->
                <circle cx="300" cy="120" r="5" fill="#171717" stroke="#bef264" stroke-width="2" />
                <circle cx="500" cy="40" r="5" fill="#171717" stroke="#bef264" stroke-width="2" />
                <circle cx="600" cy="90" r="5" fill="#171717" stroke="#bef264" stroke-width="2" />
                <circle cx="800" cy="20" r="5" fill="#171717" stroke="#bef264" stroke-width="2" />
              </svg>
              <!-- X Axis Labels -->
              <div class="absolute bottom-[-20px] left-0 right-0 flex justify-between text-[10px] font-mono text-gray-500">
                <span>JAN</span>
                <span>FEB</span>
                <span>MAR</span>
                <span>APR</span>
                <span>MAY</span>
                <span>JUN</span>
              </div>
            </div>
          </div>

          <!-- Active Project Progress -->
          <div class="bg-[#171717] border border-white/[0.08] rounded-xl p-6">
            <div class="flex justify-between items-center mb-6">
              <h3 class="font-display font-bold text-white text-lg">Active Projects</h3>
              <NuxtLink to="/projects" class="text-xs text-[#bef264] hover:underline">View All</NuxtLink>
            </div>
            
            <div class="space-y-6">
              <div v-for="(project, index) in activeProjects" :key="project.id" class="space-y-2">
                <div class="flex justify-between items-center">
                  <div>
                    <h4 class="font-bold text-white text-sm">{{ project.name }}</h4>
                    <p class="text-xs text-gray-400">Due in {{ (index + 1) * 3 }} days</p>
                  </div>
                  <span class="text-xs font-mono text-white">{{ 100 - ((index + 1) * 20) }}%</span>
                </div>
                <div class="w-full bg-white/5 rounded-full h-2">
                  <div class="bg-[#bef264] h-2 rounded-full transition-all duration-1000" :style="{ width: `${100 - ((index + 1) * 20)}%` }"></div>
                </div>
              </div>

              <div v-if="activeProjects.length === 0" class="text-center text-sm text-gray-500 py-4">
                No active projects found.
              </div>
            </div>
          </div>

        </div>

        <!-- Right Column: Quick Actions & Timeline -->
        <div class="lg:col-span-1 space-y-8">
          
          <!-- Quick Actions -->
          <div class="bg-[#171717] border border-white/[0.08] rounded-xl p-6">
            <h3 class="font-display font-bold text-white text-lg mb-4">Quick Actions</h3>
            <div class="grid grid-cols-2 gap-3">
              <button class="bg-[#1e2020] hover:bg-white/10 border border-white/5 p-4 rounded-lg flex flex-col items-center justify-center gap-2 transition-all group">
                <span class="material-symbols-outlined text-gray-400 group-hover:text-[#bef264]">person_add</span>
                <span class="text-xs font-semibold text-gray-300">Add Client</span>
              </button>
              <button class="bg-[#1e2020] hover:bg-white/10 border border-white/5 p-4 rounded-lg flex flex-col items-center justify-center gap-2 transition-all group">
                <span class="material-symbols-outlined text-gray-400 group-hover:text-[#bef264]">receipt</span>
                <span class="text-xs font-semibold text-gray-300">Create Invoice</span>
              </button>
              <button class="bg-[#1e2020] hover:bg-white/10 border border-white/5 p-4 rounded-lg flex flex-col items-center justify-center gap-2 transition-all group">
                <span class="material-symbols-outlined text-gray-400 group-hover:text-[#bef264]">description</span>
                <span class="text-xs font-semibold text-gray-300">Send Proposal</span>
              </button>
              <button class="bg-[#1e2020] hover:bg-white/10 border border-white/5 p-4 rounded-lg flex flex-col items-center justify-center gap-2 transition-all group">
                <span class="material-symbols-outlined text-gray-400 group-hover:text-[#bef264]">add_task</span>
                <span class="text-xs font-semibold text-gray-300">Add Task</span>
              </button>
            </div>
          </div>

          <!-- Activity Timeline -->
          <div class="bg-[#171717] border border-white/[0.08] rounded-xl p-6">
            <div class="flex justify-between items-center mb-6">
              <h3 class="font-display font-bold text-white text-lg">Recent Activity</h3>
            </div>
            
            <div class="space-y-6 relative before:absolute before:inset-0 before:ml-4 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-white/10 before:to-transparent">
              
              <!-- Item 1 -->
              <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div class="flex items-center justify-center w-8 h-8 rounded-full border border-white/10 bg-[#1e2020] text-gray-400 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow">
                  <span class="material-symbols-outlined text-[14px]">comment</span>
                </div>
                <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-lg border border-white/5 bg-[#1e2020]">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-white text-xs">New Comment</span>
                    <span class="text-[10px] text-gray-500">2 hrs ago</span>
                  </div>
                  <div class="text-xs text-gray-400">Client left a comment on Homepage Design v2</div>
                </div>
              </div>

              <!-- Item 2 -->
              <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div class="flex items-center justify-center w-8 h-8 rounded-full border border-white/10 bg-[#1e2020] text-gray-400 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow">
                  <span class="material-symbols-outlined text-[14px] text-[#bef264]">check_circle</span>
                </div>
                <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-lg border border-white/5 bg-[#1e2020]">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-white text-xs">Invoice Paid</span>
                    <span class="text-[10px] text-gray-500">5 hrs ago</span>
                  </div>
                  <div class="text-xs text-gray-400">Invoice #0045 was paid successfully.</div>
                </div>
              </div>

              <!-- Item 3 -->
              <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div class="flex items-center justify-center w-8 h-8 rounded-full border border-white/10 bg-[#1e2020] text-gray-400 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow">
                  <span class="material-symbols-outlined text-[14px]">dynamic_form</span>
                </div>
                <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-lg border border-white/5 bg-[#1e2020]">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-white text-xs">Form Submitted</span>
                    <span class="text-[10px] text-gray-500">1 day ago</span>
                  </div>
                  <div class="text-xs text-gray-400">Onboarding questionnaire completed.</div>
                </div>
              </div>

            </div>
          </div>

        </div>

      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'

const authStore = useAuthStore()
const api = useApi()

const projects = ref([])
const clients = ref([])
const isLoading = ref(true)

const activeProjects = computed(() => {
  return projects.value.filter(p => p.status === 'active' || p.status === 'In Progress')
})

onMounted(async () => {
  try {
    const [projectsData, clientsData] = await Promise.all([
      api('/api/v1/projects').catch(() => []),
      api('/api/v1/clients').catch(() => [])
    ])
    projects.value = projectsData || []
    clients.value = clientsData || []
  } catch (error) {
    console.error('Failed to fetch dashboard data', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
/* Timeline specific styles to ensure line connects the dots nicely */
.is-active::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 1rem;
  width: 1rem;
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  z-index: -1;
}

@media (min-width: 768px) {
  .is-active::before {
    left: 50%;
    width: 2rem;
  }
  .is-active:nth-child(odd)::before {
    left: calc(50% - 2rem);
  }
}
</style>
