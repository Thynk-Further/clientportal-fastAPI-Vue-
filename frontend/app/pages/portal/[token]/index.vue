<template>
  <div class="space-y-8">
    
    <!-- Client Welcome Banner -->
    <div class="bg-gradient-to-br from-[#1c2214] to-[#121414] border border-[#bef264]/20 rounded-xl p-8 shadow-sm relative overflow-hidden">
      <!-- Decorative background element -->
      <div class="absolute -right-20 -top-20 w-64 h-64 bg-[#bef264] rounded-full blur-[100px] opacity-10 pointer-events-none"></div>
      
      <div class="relative z-10 max-w-2xl">
        <h1 class="text-3xl md:text-4xl font-display font-bold text-white tracking-tight mb-2">Secure Client Terminal</h1>
        <p class="text-sm text-gray-400 font-sans">Access active development milestones, review architectural deliverables, and process payments securely in this high-performance portal.</p>
      </div>
    </div>

    <div>
      <h2 class="text-xl font-display font-bold text-white mb-6 flex items-center gap-2">
        <span class="material-symbols-outlined text-[#bef264]">rocket_launch</span>
        Your Development Milestones
      </h2>

      <!-- Loading State -->
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="i in 2" :key="i" class="bg-[#171717] rounded-xl border border-white/5 p-6 h-48 animate-pulse"></div>
      </div>

      <!-- Empty State -->
      <div v-else-if="projects.length === 0" class="bg-[#171717] rounded-xl border border-dashed border-white/10 p-12 text-center">
        <span class="material-symbols-outlined text-4xl text-gray-400 mb-3 opacity-50">data_alert</span>
        <h3 class="text-lg font-display font-bold text-white mb-2">No projects assigned</h3>
        <p class="text-gray-400 text-xs max-w-sm mx-auto">Your account manager hasn't linked any active development channels to your profile yet.</p>
      </div>

      <!-- Projects Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <NuxtLink v-for="project in projects" :key="project.id" :to="`/portal/${route.params.token}/projects/${project.id}`" class="bg-[#171717] rounded-xl border border-white/5 p-6 hover:border-[#bef264]/20 transition-all group relative cursor-pointer flex flex-col block">
          <div class="flex justify-between items-start mb-4 gap-2">
            <div>
              <h3 class="font-bold text-white text-lg group-hover:text-[#bef264] transition-colors font-display truncate">{{ project.name }}</h3>
              <p class="text-[10px] text-gray-500 mt-1 font-mono uppercase tracking-wider">Started {{ new Date(project.created_at).toLocaleDateString() }}</p>
            </div>
            <!-- Status Badge -->
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider font-mono shrink-0"
                  :class="{
                    'bg-[#bef264]/10 text-[#bef264] border border-[#bef264]/20': project.status === 'active',
                    'bg-[#1e2020] text-gray-400 border border-white/10': project.status !== 'active'
                  }">
              {{ project.status === 'active' ? 'Active' : project.status }}
            </span>
          </div>
          
          <p class="text-sm text-gray-400 line-clamp-2 mb-6 flex-1">{{ project.description || 'No description provided.' }}</p>
          
          <div class="pt-4 border-t border-white/5 flex items-center justify-between mt-auto">
            <span class="text-xs font-bold font-mono uppercase tracking-wider text-[#bef264] group-hover:text-[#a4d64c] flex items-center transition-colors">
              Enter Milestone
              <span class="material-symbols-outlined text-sm ml-1 transition-transform group-hover:translate-x-1">arrow_forward</span>
            </span>
          </div>
        </NuxtLink>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { FolderKanban, ChevronRight } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

const route = useRoute()
const api = useApi()

const projects = ref([])
const isLoading = ref(true)

const fetchClientProjects = async () => {
  try {
    // This call uses the HttpOnly cp_session cookie we just received in the parent route!
    const data = await api('/api/v1/portal/projects')
    projects.value = data
  } catch (err) {
    console.error('Failed to fetch portal projects', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchClientProjects()
})
</script>
