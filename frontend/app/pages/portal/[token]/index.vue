<template>
  <div class="space-y-8">
    
    <!-- Client Welcome Banner -->
    <div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-sm relative overflow-hidden">
      <!-- Decorative background element -->
      <div class="absolute -right-20 -top-20 w-64 h-64 bg-indigo-50 rounded-full blur-3xl opacity-50 pointer-events-none"></div>
      
      <div class="relative z-10 max-w-2xl">
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight mb-2">Welcome to your Portal</h1>
        <p class="text-lg text-gray-600">This is your dedicated workspace. Here you can track project progress, review deliverables, and communicate directly with your freelancer.</p>
      </div>
    </div>

    <div>
      <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <FolderKanban class="w-5 h-5 text-indigo-600" />
        Your Projects
      </h2>

      <!-- Loading State -->
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="i in 2" :key="i" class="bg-white rounded-2xl border border-gray-100 p-6 h-48 animate-pulse"></div>
      </div>

      <!-- Empty State (Should rarely happen since they were just invited) -->
      <div v-else-if="projects.length === 0" class="bg-white rounded-3xl border border-dashed border-gray-300 p-12 text-center">
        <h3 class="text-lg font-bold text-gray-900 mb-2">No projects yet</h3>
        <p class="text-gray-500 max-w-sm mx-auto">Your freelancer hasn't assigned any projects to you yet. Check back soon!</p>
      </div>

      <!-- Projects Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- We use standard div instead of NuxtLink for now, until we build the client project detail view -->
        <div v-for="project in projects" :key="project.id" class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow group relative cursor-pointer flex flex-col">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="font-bold text-gray-900 text-xl group-hover:text-indigo-600 transition-colors">{{ project.name }}</h3>
              <p class="text-sm text-gray-500 mt-1">Started {{ new Date(project.created_at).toLocaleDateString() }}</p>
            </div>
            <!-- Status Badge -->
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold"
                  :class="{
                    'bg-green-100 text-green-800': project.status === 'active',
                    'bg-gray-100 text-gray-800': project.status !== 'active'
                  }">
              {{ project.status === 'active' ? 'Active' : project.status }}
            </span>
          </div>
          
          <p class="text-base text-gray-600 line-clamp-2 mb-6 flex-1">{{ project.description || 'No description provided.' }}</p>
          
          <div class="pt-4 border-t border-gray-50 flex items-center justify-between mt-auto">
            <span class="text-sm font-medium text-indigo-600 group-hover:text-indigo-700 flex items-center">
              View Project <ChevronRight class="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" />
            </span>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FolderKanban, ChevronRight } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

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
