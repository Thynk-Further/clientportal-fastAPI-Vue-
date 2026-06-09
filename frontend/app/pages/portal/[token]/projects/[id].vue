<template>
  <div class="space-y-6">
    
    <!-- Back Navigation -->
    <div class="flex items-center gap-2 mb-4">
      <NuxtLink :to="`/portal/${route.params.token}`" class="inline-flex items-center text-sm font-medium text-gray-400 hover:text-white transition-colors">
        <ArrowLeft class="w-4 h-4 mr-1" />
        Back to Dashboard
      </NuxtLink>
    </div>

    <!-- Loading State for Project Header -->
    <div v-if="isLoadingProject" class="animate-pulse flex items-center gap-4">
      <div class="w-12 h-12 bg-layer-2 rounded-xl"></div>
      <div class="space-y-2">
        <div class="h-6 bg-layer-2 rounded w-48"></div>
        <div class="h-4 bg-layer-2/50 rounded w-32"></div>
      </div>
    </div>

    <!-- Project Header -->
    <div v-else-if="project" class="bg-layer-1 rounded-3xl border border-white/5 p-8 shadow-sm relative overflow-hidden">
      <!-- Decorative element -->
      <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-accent rounded-full blur-[80px] opacity-20 pointer-events-none"></div>

      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <h1 class="text-3xl font-bold text-white tracking-tight font-heading">{{ project.name }}</h1>
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold font-mono"
                :class="{
                  'bg-accent/20 text-accent': project.status === 'active',
                  'bg-layer-2 text-gray-400 border border-white/10': project.status !== 'active'
                }">
            {{ project.status === 'active' ? 'Active' : project.status }}
          </span>
        </div>
        <p class="text-lg text-gray-400 max-w-3xl">{{ project.description || 'No description provided.' }}</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-900/20 p-6 rounded-2xl border border-red-900/50 text-center">
      <p class="text-red-400">{{ error }}</p>
    </div>

    <!-- Deliverables Section -->
    <div v-if="project" class="mt-10">
      <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2 font-heading">
        <FileBox class="w-5 h-5 text-accent" />
        Deliverables
      </h2>

      <!-- Loading Deliverables -->
      <div v-if="isLoadingDeliverables" class="space-y-4">
        <div v-for="i in 3" :key="i" class="bg-layer-1 rounded-2xl border border-white/5 p-5 h-24 animate-pulse"></div>
      </div>

      <!-- Empty Deliverables -->
      <div v-else-if="deliverables.length === 0" class="bg-layer-1 rounded-3xl border border-dashed border-white/10 p-12 text-center">
        <div class="w-16 h-16 bg-layer-2 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <FileBox class="w-8 h-8 text-gray-500" />
        </div>
        <h3 class="text-lg font-bold text-white mb-2 font-heading">No deliverables yet</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Your freelancer is still preparing work for this project. Check back later!</p>
      </div>

      <!-- Deliverables List -->
      <div v-else class="space-y-4">
        <!-- Currently just divs, later they might be clickable if we want a separate view for each deliverable, or expanding accordions -->
        <div v-for="deliverable in deliverables" :key="deliverable.id" class="bg-layer-1 rounded-2xl border border-white/5 p-6 hover:bg-layer-2 transition-colors group">
          <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
            <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-layer-2 text-accent rounded-xl flex items-center justify-center shrink-0 border border-white/10">
              <FileBox class="w-6 h-6" />
            </div>
            <div>
              <h3 class="font-bold text-white text-xl group-hover:text-accent transition-colors font-heading">{{ deliverable.name }}</h3>
              <p class="text-sm text-gray-400 mt-1">{{ deliverable.description || 'No description' }}</p>
              <div class="flex items-center gap-4 mt-3">
                <span class="inline-flex items-center text-xs font-medium text-gray-500 font-mono">
                  <Clock class="w-3.5 h-3.5 mr-1 text-gray-500" />
                  v{{ deliverable.version }}
                </span>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold font-mono"
                      :class="{
                        'bg-yellow-900/30 text-yellow-500 border border-yellow-900/50': deliverable.status === 'draft',
                        'bg-blue-900/30 text-blue-400 border border-blue-900/50': deliverable.status === 'in_review',
                        'bg-accent/20 text-accent border border-accent/20': deliverable.status === 'approved',
                        'bg-red-900/30 text-red-400 border border-red-900/50': deliverable.status === 'changes_requested'
                      }">
                  {{ deliverable.status.replace('_', ' ').toUpperCase() }}
                </span>
              </div>
            </div>
          </div>
          
          
          <!-- Actions (Placeholder for now) -->
          <button class="px-4 py-2 text-sm font-medium text-layer-0 bg-accent rounded-lg hover:bg-[#a4d64c] transition-colors shrink-0">
            Leave Feedback
          </button>
          </div>

          <!-- Uploaded Files List -->
          <div v-if="deliverable.file_uploads && deliverable.file_uploads.length > 0" class="mt-4 pt-4 border-t border-white/5 space-y-2">
            <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 font-mono">Attached Files</h4>
            <div v-for="file in deliverable.file_uploads" :key="file.id" class="flex items-center justify-between p-3 bg-layer-2 rounded-lg border border-white/5 group/file hover:bg-[#2e2e2e] transition-colors cursor-pointer">
              <div class="flex items-center gap-3">
                <FileText class="w-4 h-4 text-accent" />
                <span class="text-sm font-medium text-gray-200 group-hover/file:text-accent transition-colors">{{ file.file_name }}</span>
                <span class="text-xs text-gray-500 font-mono">({{ Math.round(file.file_size / 1024) }} KB)</span>
              </div>
              <button class="text-sm font-medium text-accent hover:text-[#a4d64c] opacity-0 group-hover/file:opacity-100 transition-opacity">Download</button>
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
