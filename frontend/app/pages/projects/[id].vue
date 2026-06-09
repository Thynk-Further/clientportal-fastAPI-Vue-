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

      <!-- Navigation Tabs -->
      <div class="mt-8 border-b border-white/5">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button 
            @click="activeTab = 'milestones'"
            class="whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium font-mono transition-colors"
            :class="activeTab === 'milestones' ? 'border-accent text-accent' : 'border-transparent text-gray-500 hover:border-gray-400 hover:text-gray-300'">
            Milestones
          </button>
          <button 
            @click="activeTab = 'deliverables'"
            class="whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium font-mono transition-colors"
            :class="activeTab === 'deliverables' ? 'border-accent text-accent' : 'border-transparent text-gray-500 hover:border-gray-400 hover:text-gray-300'">
            Deliverables
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

    <!-- Milestones Content -->
    <div v-if="project && activeTab === 'milestones'" class="space-y-6 animate-in fade-in duration-300">
      
      <!-- Header -->
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-white font-heading">Project Milestones</h2>
        <button @click="isMilestoneModalOpen = true" class="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium text-layer-0 bg-accent rounded-lg hover:bg-[#a4d64c] transition-colors">
          <Plus class="w-4 h-4 mr-1.5" />
          Add Milestone
        </button>
      </div>

      <!-- Loading Milestones -->
      <div v-if="isLoadingMilestones" class="space-y-4">
        <div v-for="i in 3" :key="i" class="bg-layer-1 rounded-2xl border border-white/5 p-5 h-20 animate-pulse"></div>
      </div>

      <!-- Empty Milestones -->
      <div v-else-if="milestones.length === 0" class="bg-layer-1 rounded-3xl border border-dashed border-white/10 p-12 text-center">
        <div class="w-16 h-16 bg-layer-2 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <span class="material-symbols-outlined text-gray-500 text-3xl">event_note</span>
        </div>
        <h3 class="text-lg font-bold text-white mb-2 font-heading">No milestones scheduled</h3>
        <p class="text-gray-400 max-w-sm mx-auto mb-6">Create milestones to give your client a clear timeline and track project progress.</p>
        <button @click="isMilestoneModalOpen = true" class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-layer-0 bg-accent rounded-lg hover:bg-[#a4d64c] transition-colors">
          <Plus class="w-4 h-4 mr-2" />
          Add Milestone
        </button>
      </div>

      <!-- Milestones List -->
      <div v-else class="space-y-4">
        <div v-for="milestone in milestones" :key="milestone.id" class="bg-layer-1 rounded-2xl border border-white/5 p-6 hover:bg-layer-2 transition-colors flex items-center justify-between gap-4 group">
          <div class="flex items-center gap-4">
            <button @click="toggleMilestoneStatus(milestone)" class="w-6 h-6 rounded-full border-2 flex items-center justify-center shrink-0 transition-colors"
                 :class="milestone.status === 'completed' ? 'border-green-500 bg-green-500 text-white' : 'border-gray-500 text-transparent hover:border-accent'">
              <span class="material-symbols-outlined text-sm font-bold" v-if="milestone.status === 'completed'">check</span>
            </button>
            <div>
              <h3 class="font-bold text-white text-lg font-heading" :class="{'line-through text-gray-500': milestone.status === 'completed'}">{{ milestone.title }}</h3>
              <p class="text-sm text-gray-400 mt-1" v-if="milestone.description">{{ milestone.description }}</p>
              <div class="text-xs font-mono text-gray-500 mt-2" v-if="milestone.due_date">Due: {{ new Date(milestone.due_date).toLocaleDateString() }}</div>
            </div>
          </div>
          
          <div class="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-2">
            <button @click="deleteMilestone(milestone.id)" class="p-2 text-gray-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors">
              <span class="material-symbols-outlined text-[20px]">delete</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Deliverables Content -->
    <div v-if="project && activeTab === 'deliverables'" class="space-y-6 animate-in fade-in duration-300">
      
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

    <!-- Modals -->
    <AddDeliverableModal 
      v-if="project"
      :is-open="isModalOpen" 
      :project-id="project.id" 
      @close="isModalOpen = false" 
      @deliverable-added="handleDeliverableAdded" 
    />

    <AddMilestoneModal
      v-if="project"
      :is-open="isMilestoneModalOpen"
      :project-id="project.id"
      @close="isMilestoneModalOpen = false"
      @milestone-added="handleMilestoneAdded"
    />
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { FolderKanban, Plus, FileBox, Clock, ChevronRight, FileText } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'
import AddDeliverableModal from '~/components/AddDeliverableModal.vue'
import AddMilestoneModal from '~/components/AddMilestoneModal.vue'
import FileUpload from '~/components/FileUpload.vue'

const route = useRoute()
const projectId = route.params.id
const api = useApi()

// State
const project = ref(null)
const isLoadingProject = ref(true)
const error = ref(null)

const activeTab = ref('milestones')

const deliverables = ref([])
const isLoadingDeliverables = ref(true)

const milestones = ref([])
const isLoadingMilestones = ref(true)

const isModalOpen = ref(false)
const isMilestoneModalOpen = ref(false)

const fetchProjectData = async () => {
  try {
    // Fetch project metadata
    project.value = await api(`/api/v1/projects/${projectId}`)
    
    // Fetch deliverables
    deliverables.value = await api(`/api/v1/projects/${projectId}/deliverables`)

    // Fetch milestones
    milestones.value = await api(`/api/v1/projects/${projectId}/milestones`)

  } catch (err) {
    console.error('Failed to fetch project details', err)
    error.value = 'Could not load project. It may have been deleted or you do not have access.'
  } finally {
    isLoadingProject.value = false
    isLoadingDeliverables.value = false
    isLoadingMilestones.value = false
  }
}

const handleDeliverableAdded = (newDeliverable) => {
  deliverables.value.push(newDeliverable)
}

const handleMilestoneAdded = (newMilestone) => {
  milestones.value.push(newMilestone)
}

const toggleMilestoneStatus = async (milestone) => {
  const originalStatus = milestone.status
  const newStatus = originalStatus === 'pending' ? 'completed' : 'pending'
  
  // Optimistic update
  milestone.status = newStatus

  try {
    await api(`/api/v1/projects/${projectId}/milestones/${milestone.id}`, {
      method: 'PATCH',
      body: { status: newStatus }
    })
  } catch (err) {
    console.error('Failed to update milestone status', err)
    milestone.status = originalStatus // Revert on failure
  }
}

const deleteMilestone = async (milestoneId) => {
  if (!confirm('Are you sure you want to delete this milestone?')) return
  
  try {
    await api(`/api/v1/projects/${projectId}/milestones/${milestoneId}`, {
      method: 'DELETE'
    })
    milestones.value = milestones.value.filter(m => m.id !== milestoneId)
  } catch (err) {
    console.error('Failed to delete milestone', err)
    alert('Failed to delete milestone')
  }
}

onMounted(() => {
  fetchProjectData()
})
</script>
