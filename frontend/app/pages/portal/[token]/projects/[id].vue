<template>
  <div class="space-y-6">
    
    <!-- Back Navigation -->
    <div class="flex items-center gap-2 mb-4">
      <NuxtLink :to="`/portal/${route.params.token}`" class="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors">
        <ArrowLeft class="w-4 h-4 mr-1" />
        Back to Dashboard
      </NuxtLink>
    </div>

    <!-- Loading State for Project Header -->
    <div v-if="isLoadingProject" class="animate-pulse flex items-center gap-4">
      <div class="w-12 h-12 bg-gray-200 rounded-xl"></div>
      <div class="space-y-2">
        <div class="h-6 bg-gray-200 rounded w-48"></div>
        <div class="h-4 bg-gray-100 rounded w-32"></div>
      </div>
    </div>

    <!-- Project Header -->
    <div v-else-if="project" class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm relative overflow-hidden">
      <!-- Decorative element -->
      <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-indigo-50 rounded-full blur-2xl opacity-60 pointer-events-none"></div>

      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <h1 class="text-3xl font-bold text-gray-900 tracking-tight">{{ project.name }}</h1>
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold"
                :class="{
                  'bg-green-100 text-green-800': project.status === 'active',
                  'bg-gray-100 text-gray-800': project.status !== 'active'
                }">
            {{ project.status === 'active' ? 'Active' : project.status }}
          </span>
        </div>
        <p class="text-lg text-gray-600 max-w-3xl">{{ project.description || 'No description provided.' }}</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 p-6 rounded-2xl border border-red-100 text-center">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <!-- Deliverables Section -->
    <div v-if="project" class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <FileBox class="w-5 h-5 text-indigo-600" />
        Deliverables
      </h2>

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
        <p class="text-gray-500 max-w-sm mx-auto">Your freelancer is still preparing work for this project. Check back later!</p>
      </div>

      <!-- Deliverables List -->
      <div v-else class="space-y-4">
        <!-- Currently just divs, later they might be clickable if we want a separate view for each deliverable, or expanding accordions -->
        <div v-for="deliverable in deliverables" :key="deliverable.id" class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow group">
          <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
            <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center shrink-0">
              <FileBox class="w-6 h-6" />
            </div>
            <div>
              <h3 class="font-bold text-gray-900 text-xl group-hover:text-indigo-600 transition-colors">{{ deliverable.name }}</h3>
              <p class="text-sm text-gray-600 mt-1">{{ deliverable.description || 'No description' }}</p>
              <div class="flex items-center gap-4 mt-3">
                <span class="inline-flex items-center text-xs font-medium text-gray-500">
                  <Clock class="w-3.5 h-3.5 mr-1 text-gray-400" />
                  v{{ deliverable.version }}
                </span>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold"
                      :class="{
                        'bg-yellow-100 text-yellow-800 border border-yellow-200': deliverable.status === 'draft',
                        'bg-blue-100 text-blue-800 border border-blue-200': deliverable.status === 'in_review',
                        'bg-green-100 text-green-800 border border-green-200': deliverable.status === 'approved',
                        'bg-red-100 text-red-800 border border-red-200': deliverable.status === 'changes_requested'
                      }">
                  {{ deliverable.status.replace('_', ' ').toUpperCase() }}
                </span>
              </div>
            </div>
          </div>
          
          
          <!-- Actions (Placeholder for now) -->
          <button class="px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors shrink-0">
            Leave Feedback
          </button>
          </div>

          <!-- Uploaded Files List -->
          <div v-if="deliverable.file_uploads && deliverable.file_uploads.length > 0" class="mt-4 pt-4 border-t border-gray-50 space-y-2">
            <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Attached Files</h4>
            <div v-for="file in deliverable.file_uploads" :key="file.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-100 group/file hover:bg-gray-100 transition-colors cursor-pointer">
              <div class="flex items-center gap-3">
                <FileText class="w-4 h-4 text-indigo-500" />
                <span class="text-sm font-medium text-gray-700 group-hover/file:text-indigo-600 transition-colors">{{ file.file_name }}</span>
                <span class="text-xs text-gray-400">({{ Math.round(file.file_size / 1024) }} KB)</span>
              </div>
              <button class="text-sm font-medium text-indigo-600 hover:text-indigo-700 opacity-0 group-hover/file:opacity-100 transition-opacity">Download</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, FileBox, Clock, FileText } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

const route = useRoute()
const projectId = route.params.id
const api = useApi()

const project = ref(null)
const isLoadingProject = ref(true)
const error = ref(null)

const deliverables = ref([])
const isLoadingDeliverables = ref(true)

const fetchProjectData = async () => {
  try {
    // Fetch project metadata
    project.value = await api(`/api/v1/portal/projects/${projectId}`)
    
    // Fetch deliverables
    deliverables.value = await api(`/api/v1/portal/projects/${projectId}/deliverables`)
  } catch (err) {
    console.error('Failed to fetch project details', err)
    error.value = 'Could not load project. It may have been deleted.'
  } finally {
    isLoadingProject.value = false
    isLoadingDeliverables.value = false
  }
}

onMounted(() => {
  fetchProjectData()
})
</script>
