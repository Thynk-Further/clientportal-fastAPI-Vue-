<template>
  <div class="max-w-6xl mx-auto space-y-6">
    
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Projects</h1>
        <p class="mt-1 text-sm text-gray-500">Manage all your client projects in one place.</p>
      </div>
      <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shrink-0">
        <Plus class="w-5 h-5 mr-1.5" />
        Create Project
      </button>
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
      <div class="w-16 h-16 bg-indigo-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <FolderKanban class="w-8 h-8 text-indigo-600" />
      </div>
      <h3 class="text-lg font-bold text-gray-900 mb-2">No projects found</h3>
      <p class="text-gray-500 max-w-sm mx-auto mb-6">You haven't created any projects yet. Create your first project to start managing deliverables.</p>
      <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">
        <Plus class="w-4 h-4 mr-2" />
        Create Project
      </button>
    </div>

    <!-- Projects Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <NuxtLink v-for="project in projects" :key="project.id" :to="'/projects/' + project.id" class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow group relative cursor-pointer flex flex-col block">
        <div class="flex justify-between items-start mb-2">
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
        
        <p class="text-sm text-gray-500 line-clamp-2 mb-4 flex-1">{{ project.description || 'No description provided.' }}</p>
        
        <div class="pt-4 border-t border-gray-50 flex items-center justify-between mt-auto">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 rounded-full bg-indigo-100 flex items-center justify-center">
              <Users class="w-3.5 h-3.5 text-indigo-600" />
            </div>
            <span class="text-xs text-gray-600 font-medium">Assigned</span>
          </div>
          <span class="text-xs text-gray-400 font-medium">Created {{ new Date(project.created_at).toLocaleDateString() }}</span>
        </div>
      </NuxtLink>
    </div>

    <!-- The Add Project Modal Component -->
    <AddProjectModal :is-open="isModalOpen" @close="isModalOpen = false" @project-added="handleProjectAdded" />
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, FolderKanban, Users } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'
import AddProjectModal from '~/components/AddProjectModal.vue'

const api = useApi()

const projects = ref([])
const isLoading = ref(true)
const isModalOpen = ref(false)

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

const handleProjectAdded = (newProject) => {
  // Push the newly created project into the list so we don't have to refetch
  projects.value.unshift(newProject)
}

onMounted(() => {
  fetchProjects()
})
</script>
