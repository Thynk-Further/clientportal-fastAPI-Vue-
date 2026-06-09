<template>
  <div class="max-w-6xl mx-auto space-y-6">
    
    <!-- Loading State for Project Header -->
    <div v-if="isLoadingProject" class="animate-pulse flex items-center gap-4">
      <div class="w-12 h-12 bg-layer-2 rounded-xl"></div>
      <div class="space-y-2">
        <div class="h-6 bg-layer-2 rounded w-48"></div>
        <div class="h-4 bg-layer-2/50 rounded w-32"></div>
      </div>
    </div>

    <!-- Project Header -->
    <div v-else-if="project" class="bg-layer-1 rounded-2xl border border-white/5 p-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 bg-layer-2 text-accent rounded-xl flex items-center justify-center shrink-0 border border-white/10">
            <FolderKanban class="w-7 h-7" />
          </div>
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h1 class="text-2xl font-bold text-white tracking-tight font-heading">{{ project.name }}</h1>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-mono"
                    :class="{
                      'bg-accent/20 text-accent': project.status === 'active',
                      'bg-layer-2 text-gray-400 border border-white/10': project.status !== 'active'
                    }">
                {{ project.status || 'Active' }}
              </span>
            </div>
            <p class="text-sm text-gray-400">{{ project.description || 'No description provided.' }}</p>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs (Only Deliverables is active for now) -->
      <div class="mt-8 border-b border-white/5">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button class="whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium border-accent text-accent font-mono">
            Deliverables
          </button>
          <button class="whitespace-nowrap border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:border-gray-400 hover:text-gray-300 cursor-not-allowed opacity-50 font-mono" title="Coming soon">
            Invoices
          </button>
          <button class="whitespace-nowrap border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:border-gray-400 hover:text-gray-300 cursor-not-allowed opacity-50 font-mono" title="Coming soon">
            Time Tracking
          </button>
        </nav>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-900/20 p-6 rounded-2xl border border-red-900/50 text-center">
      <p class="text-red-400">{{ error }}</p>
      <NuxtLink to="/projects" class="mt-4 inline-block text-accent hover:text-[#a4d64c] font-medium text-sm">
        &larr; Back to Projects
      </NuxtLink>
    </div>

    <!-- Deliverables Content -->
    <div v-if="project" class="space-y-6">
      
      <!-- Deliverables Header -->
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-white font-heading">Deliverables</h2>
        <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium text-layer-0 bg-accent rounded-lg hover:bg-[#a4d64c] transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#a4d64c]">
          <Plus class="w-4 h-4 mr-1.5" />
          Add Deliverable
        </button>
      </div>

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
        <p class="text-gray-400 max-w-sm mx-auto mb-6">Create a deliverable to start uploading files, collecting feedback, and getting approvals from your client.</p>
        <button @click="isModalOpen = true" class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-layer-0 bg-accent rounded-lg hover:bg-[#a4d64c] transition-colors">
          <Plus class="w-4 h-4 mr-2" />
          Add Deliverable
        </button>
      </div>

      <!-- Deliverables List -->
      <div v-else class="space-y-4">
        <div v-for="deliverable in deliverables" :key="deliverable.id" class="bg-layer-1 rounded-2xl border border-white/5 p-5 hover:bg-layer-2 transition-colors group">
          <div class="flex items-start justify-between gap-4">
            <div class="flex items-start gap-4 flex-1">
              <div class="w-10 h-10 bg-layer-2 text-accent rounded-lg flex items-center justify-center shrink-0 mt-1 border border-white/10">
                <FileBox class="w-5 h-5" />
              </div>
              <div>
                <h3 class="font-bold text-white text-lg group-hover:text-accent transition-colors font-heading">{{ deliverable.name }}</h3>
                <p class="text-sm text-gray-400 mt-1">{{ deliverable.description || 'No description' }}</p>
                <div class="flex items-center gap-4 mt-3">
                  <span class="inline-flex items-center text-xs font-medium text-gray-500 font-mono">
                    <Clock class="w-3.5 h-3.5 mr-1 text-gray-500" />
                    v{{ deliverable.version }}
                  </span>
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium font-mono"
                        :class="{
                          'bg-yellow-900/30 text-yellow-500 border border-yellow-900/50': deliverable.status === 'draft',
                          'bg-blue-900/30 text-blue-400 border border-blue-900/50': deliverable.status === 'in_review',
                          'bg-accent/20 text-accent border border-accent/20': deliverable.status === 'approved',
                          'bg-red-900/30 text-red-400 border border-red-900/50': deliverable.status === 'changes_requested'
                        }">
                    {{ deliverable.status.replace('_', ' ') }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <button class="text-sm font-medium text-accent hover:text-[#a4d64c] flex items-center shrink-0">
              Open <ChevronRight class="w-4 h-4 ml-1" />
            </button>
          </div>

          <!-- Uploaded Files List -->
          <div v-if="deliverable.file_uploads && deliverable.file_uploads.length > 0" class="mt-4 pt-4 border-t border-white/5 space-y-2">
            <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 font-mono">Attached Files</h4>
            <div v-for="file in deliverable.file_uploads" :key="file.id" class="flex items-center justify-between p-3 bg-layer-2 rounded-lg border border-white/5 group/file hover:bg-[#2e2e2e] transition-colors">
              <div class="flex items-center gap-3">
                <FileText class="w-4 h-4 text-accent" />
                <span class="text-sm font-medium text-gray-200">{{ file.file_name }}</span>
                <span class="text-xs text-gray-500 font-mono">({{ Math.round(file.file_size / 1024) }} KB)</span>
              </div>
            </div>
          </div>

          <!-- File Upload Component -->
          <FileUpload 
            :deliverable-id="deliverable.id" 
            @upload-complete="(newFile) => { deliverable.file_uploads = deliverable.file_uploads || []; deliverable.file_uploads.push(newFile) }" 
          />
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
import { FolderKanban, Plus, FileBox, Clock, ChevronRight, FileText } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'
import AddDeliverableModal from '~/components/AddDeliverableModal.vue'
import FileUpload from '~/components/FileUpload.vue'

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
