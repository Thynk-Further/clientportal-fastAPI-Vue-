<template>
  <div class="max-w-6xl mx-auto space-y-8">
    
    <!-- Dashboard Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Overview</h1>
      <p class="mt-2 text-sm text-gray-500">Welcome back, {{ authStore.user?.full_name?.split(' ')[0] || 'there' }}! Here's what's happening with your projects.</p>
    </div>

    <!-- Stats Row (Placeholder stats for now until backend supports aggregates) -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center gap-4">
        <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
          <FolderKanban class="w-6 h-6" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">Active Projects</p>
          <p class="text-2xl font-bold text-gray-900">{{ projects.length }}</p>
        </div>
      </div>
      
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center gap-4">
        <div class="w-12 h-12 bg-green-50 text-green-600 rounded-xl flex items-center justify-center">
          <CheckCircle2 class="w-6 h-6" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">Deliverables Approved</p>
          <p class="text-2xl font-bold text-gray-900">0</p>
        </div>
      </div>
      
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center gap-4">
        <div class="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center">
          <DollarSign class="w-6 h-6" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">Unpaid Invoices</p>
          <p class="text-2xl font-bold text-gray-900">$0.00</p>
        </div>
      </div>
    </div>

    <!-- Recent Projects Section -->
    <div>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-gray-900">Recent Projects</h2>
        <NuxtLink to="/projects" class="text-sm font-medium text-indigo-600 hover:text-indigo-700">
          View all
        </NuxtLink>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="bg-white rounded-2xl border border-gray-100 p-6 h-40 animate-pulse">
          <div class="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div class="h-3 bg-gray-100 rounded w-full mb-2"></div>
          <div class="h-3 bg-gray-100 rounded w-3/4"></div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="projects.length === 0" class="bg-white rounded-3xl border border-dashed border-gray-300 p-12 text-center">
        <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <FolderKanban class="w-8 h-8 text-gray-400" />
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-2">No projects yet</h3>
        <p class="text-gray-500 max-w-sm mx-auto mb-6">Get started by creating your first project and inviting a client to their portal.</p>
        <button class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">
          <Plus class="w-4 h-4 mr-2" />
          Create Project
        </button>
      </div>

      <!-- Projects Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="project in projects" :key="project.id" class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow group relative cursor-pointer">
          <div class="flex justify-between items-start mb-4">
            <h3 class="font-bold text-gray-900 text-lg group-hover:text-indigo-600 transition-colors line-clamp-1">{{ project.name }}</h3>
            <!-- Status Badge -->
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-800': project.status === 'active',
                    'bg-gray-100 text-gray-800': project.status !== 'active'
                  }">
              {{ project.status || 'Active' }}
            </span>
          </div>
          <p class="text-sm text-gray-500 line-clamp-2 mb-6">{{ project.description || 'No description provided.' }}</p>
          
          <div class="pt-4 border-t border-gray-50 flex items-center justify-between mt-auto">
            <span class="text-xs text-gray-400 font-medium">Created {{ new Date(project.created_at).toLocaleDateString() }}</span>
            <ChevronRight class="w-4 h-4 text-gray-400 group-hover:text-indigo-600 transition-colors" />
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'
import { FolderKanban, CheckCircle2, DollarSign, Plus, ChevronRight } from 'lucide-vue-next'

const authStore = useAuthStore()
const api = useApi()

const projects = ref([])
const isLoading = ref(true)

// Fetch projects when the dashboard loads
onMounted(async () => {
  try {
    const data = await api('/api/v1/projects')
    projects.value = data
  } catch (error) {
    console.error('Failed to fetch projects', error)
  } finally {
    isLoading.value = false
  }
})
</script>
