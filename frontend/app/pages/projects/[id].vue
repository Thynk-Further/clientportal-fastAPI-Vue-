<template>
  <div class="max-w-6xl mx-auto space-y-6">
    
    <!-- Loading State for Project Header -->
    <div v-if="isLoadingProject" class="animate-pulse flex items-center gap-4">
      <div class="w-12 h-12 bg-gray-200 rounded-xl"></div>
      <div class="space-y-2">
        <div class="h-6 bg-gray-200 rounded w-48"></div>
        <div class="h-4 bg-gray-100 rounded w-32"></div>
      </div>
    </div>

    <!-- Project Header -->
    <div v-else-if="project" class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center shrink-0">
            <FolderKanban class="w-7 h-7" />
          </div>
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h1 class="text-2xl font-bold text-gray-900 tracking-tight">{{ project.name }}</h1>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="{
                      'bg-green-100 text-green-800': project.status === 'active',
                      'bg-gray-100 text-gray-800': project.status !== 'active'
                    }">
                {{ project.status || 'Active' }}
              </span>
            </div>
            <p class="text-sm text-gray-500">{{ project.description || 'No description provided.' }}</p>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs (Only Deliverables is active for now) -->
      <div class="mt-8 border-b border-gray-100">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button class="whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium border-indigo-500 text-indigo-600">
            Deliverables
          </button>
          <button class="whitespace-nowrap border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700 cursor-not-allowed opacity-50" title="Coming soon">
            Invoices
          </button>
          <button class="whitespace-nowrap border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700 cursor-not-allowed opacity-50" title="Coming soon">
            Time Tracking
          </button>
        </nav>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 p-6 rounded-2xl border border-red-100 text-center">
      <p class="text-red-700">{{ error }}</p>
      <NuxtLink to="/projects" class="mt-4 inline-block text-indigo-600 hover:text-indigo-700 font-medium text-sm">
        &larr; Back to Projects
      </NuxtLink>
    </div>

    <!-- Deliverables Content -->
    <div v-if="project" class="space-y-6">
      
      <!-- Deliverables Header -->
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-gray-900">Deliverables</h2>
        <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          <Plus class="w-4 h-4 mr-1.5" />
          Add Deliverable
        </button>
      </div>

      <!-- Loading Deliverables -->
      <div v-if="isLoadingDeliverables" class="space-y-4">
        <div v-for="i in 3" :key="i" class="bg-white rounded-2xl border border-gray-100 p-5 h-24 animate-pulse"></div>
      </div>

      <!-- Empty Deliverables -->
      <div v-else-if="deliverables.length === 0" class="bg-white rounded-3xl border border-dashed border-gray-300 p-12 text-center">
        <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <FileBox class="w-8 h-8 text-gray-400" />
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-2">No deliverables yet</h3>
        <p class="text-gray-500 max-w-sm mx-auto mb-6">Create a deliverable to start uploading files, collecting feedback, and getting approvals from your client.</p>
        <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm">
          <Plus class="w-4 h-4 mr-2" />
          Add Deliverable
        </button>
      </div>

      <!-- Deliverables List -->
      <div v-else class="space-y-4">
        <div v-for="deliverable in deliverables" :key="deliverable.id" class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-shadow group">
          <div class="flex items-start justify-between gap-4">
            <div class="flex items-start gap-4 flex-1">
              <div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-lg flex items-center justify-center shrink-0 mt-1">
                <FileBox class="w-5 h-5" />
              </div>
              <div>
                <h3 class="font-bold text-gray-900 text-lg group-hover:text-indigo-600 transition-colors">{{ deliverable.name }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ deliverable.description || 'No description' }}</p>
                <div class="flex items-center gap-4 mt-3">
                  <span class="inline-flex items-center text-xs font-medium text-gray-500">
                    <Clock class="w-3.5 h-3.5 mr-1 text-gray-400" />
                    v{{ deliverable.version }}
                  </span>
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                        :class="{
                          'bg-yellow-100 text-yellow-800 border border-yellow-200': deliverable.status === 'draft',
                          'bg-blue-100 text-blue-800 border border-blue-200': deliverable.status === 'in_review',
                          'bg-green-100 text-green-800 border border-green-200': deliverable.status === 'approved',
                          'bg-red-100 text-red-800 border border-red-200': deliverable.status === 'changes_requested'
                        }">
                    {{ deliverable.status.replace('_', ' ') }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <button class="text-sm font-medium text-indigo-600 hover:text-indigo-700 flex items-center shrink-0">
              Open <ChevronRight class="w-4 h-4 ml-1" />
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- The Add Deliverable Modal Component -->
    <AddDeliverableModal 
      v-if="project"
      :is-open="isModalOpen" 
      :project-id="project.id" 
      @close="isModalOpen = false" 
      @deliverable-added="handleDeliverableAdded" 
    />
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { FolderKanban, Plus, FileBox, Clock, ChevronRight } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'
import AddDeliverableModal from '~/components/AddDeliverableModal.vue'

const route = useRoute()
const projectId = route.params.id
const api = useApi()

// State
const project = ref(null)
const isLoadingProject = ref(true)
const error = ref(null)

const deliverables = ref([])
const isLoadingDeliverables = ref(true)

const isModalOpen = ref(false)

const fetchProjectData = async () => {
  try {
    // Fetch project metadata
    project.value = await api(`/api/v1/projects/${projectId}`)
    
    // Fetch deliverables
    deliverables.value = await api(`/api/v1/projects/${projectId}/deliverables`)
  } catch (err) {
    console.error('Failed to fetch project details', err)
    error.value = 'Could not load project. It may have been deleted or you do not have access.'
  } finally {
    isLoadingProject.value = false
    isLoadingDeliverables.value = false
  }
}

const handleDeliverableAdded = (newDeliverable) => {
  // Push the new deliverable into the list
  deliverables.value.push(newDeliverable)
}

onMounted(() => {
  fetchProjectData()
})
</script>
