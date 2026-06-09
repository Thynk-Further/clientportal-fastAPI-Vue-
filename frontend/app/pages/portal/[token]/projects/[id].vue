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

    <!-- Tab Navigation -->
    <div v-if="project" class="border-b border-white/10 flex gap-6 mt-8">
      <button 
        @click="activeTab = 'overview'" 
        class="pb-3 text-sm font-bold transition-colors font-heading uppercase tracking-wider"
        :class="activeTab === 'overview' ? 'text-accent border-b-2 border-accent' : 'text-gray-500 hover:text-white'">
        Overview & Timeline
      </button>
      <button 
        @click="activeTab = 'deliverables'" 
        class="pb-3 text-sm font-bold transition-colors font-heading uppercase tracking-wider"
        :class="activeTab === 'deliverables' ? 'text-accent border-b-2 border-accent' : 'text-gray-500 hover:text-white'">
        Deliverables
      </button>
      <button 
        @click="activeTab = 'forms'" 
        class="pb-3 text-sm font-bold transition-colors font-heading uppercase tracking-wider"
        :class="activeTab === 'forms' ? 'text-accent border-b-2 border-accent' : 'text-gray-500 hover:text-white'">
        Forms & Questionnaires
      </button>
    </div>

    <!-- Tab Content: Overview & Timeline -->
    <div v-if="project && activeTab === 'overview'" class="mt-8 space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div class="flex items-center gap-3">
        <span class="material-symbols-outlined text-accent text-2xl">timeline</span>
        <h2 class="text-xl font-bold text-white font-heading">Project Milestones</h2>
      </div>

      <div v-if="isLoadingMilestones" class="space-y-4">
        <div v-for="i in 3" :key="i" class="bg-layer-1 rounded-2xl border border-white/5 p-5 h-20 animate-pulse"></div>
      </div>
      
      <div v-else-if="milestones.length === 0" class="bg-layer-1 rounded-3xl border border-dashed border-white/10 p-12 text-center">
        <span class="material-symbols-outlined text-gray-500 text-4xl mb-4">event_note</span>
        <h3 class="text-lg font-bold text-white mb-2 font-heading">No milestones scheduled</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Project timelines and milestones will appear here once they are planned.</p>
      </div>

      <div v-else class="relative">
        <div class="absolute left-[23px] top-4 bottom-4 w-0.5 bg-white/10 hidden md:block"></div>
        <div class="space-y-6">
          <div v-for="milestone in milestones" :key="milestone.id" class="flex flex-col md:flex-row gap-4 md:gap-8 group">
            <div class="flex items-center gap-4 md:w-48 shrink-0 md:justify-end z-10 pt-2">
              <div class="text-right hidden md:block">
                <div class="text-xs font-mono font-bold text-gray-400 uppercase">{{ milestone.due_date ? new Date(milestone.due_date).toLocaleDateString() : 'TBD' }}</div>
                <div class="text-[10px] text-gray-600 font-mono" v-if="milestone.status === 'completed'">COMPLETED</div>
                <div class="text-[10px] text-accent font-mono" v-else>PENDING</div>
              </div>
              <div class="w-12 h-12 rounded-full border-4 border-[#121414] bg-layer-2 flex items-center justify-center shrink-0 shadow-sm"
                   :class="milestone.status === 'completed' ? 'text-green-400 bg-green-500/10' : 'text-gray-500'">
                <span class="material-symbols-outlined text-lg">{{ milestone.status === 'completed' ? 'check_circle' : 'radio_button_unchecked' }}</span>
              </div>
              <div class="md:hidden">
                <div class="text-xs font-mono font-bold text-gray-400 uppercase">{{ milestone.due_date ? new Date(milestone.due_date).toLocaleDateString() : 'TBD' }}</div>
                <div class="text-[10px] text-accent font-mono" v-if="milestone.status !== 'completed'">PENDING</div>
              </div>
            </div>
            <div class="bg-layer-1 flex-1 rounded-2xl border border-white/5 p-6 hover:border-white/10 transition-colors">
              <h3 class="font-bold text-white text-lg font-heading" :class="{'text-gray-400 line-through': milestone.status === 'completed'}">{{ milestone.title }}</h3>
              <p class="text-sm text-gray-400 mt-2 leading-relaxed" v-if="milestone.description">{{ milestone.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Content: Deliverables -->
    <div v-if="project && activeTab === 'deliverables'" class="mt-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div class="flex items-center gap-3 mb-6">
        <FileBox class="w-6 h-6 text-accent" />
        <h2 class="text-xl font-bold text-white font-heading">Deliverables</h2>
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
        <p class="text-gray-400 max-w-sm mx-auto">Your freelancer is still preparing work for this project. Check back later!</p>
      </div>

      <!-- Deliverables List -->
      <div v-else class="space-y-4">
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

    <!-- Tab Content: Forms & Questionnaires -->
    <div v-if="project && activeTab === 'forms'" class="mt-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div class="flex items-center gap-3 mb-6">
        <span class="material-symbols-outlined text-accent text-2xl">receipt_long</span>
        <h2 class="text-xl font-bold text-white font-heading">Forms & Questionnaires</h2>
      </div>

      <div v-if="isLoadingForms" class="space-y-4">
        <div v-for="i in 2" :key="i" class="bg-layer-1 rounded-2xl border border-white/5 p-5 h-20 animate-pulse"></div>
      </div>

      <div v-else-if="forms.length === 0" class="bg-layer-1 rounded-3xl border border-dashed border-white/10 p-12 text-center">
        <div class="w-16 h-16 bg-layer-2 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <span class="material-symbols-outlined text-gray-500 text-[32px]">post_add</span>
        </div>
        <h3 class="text-lg font-bold text-white mb-2 font-heading">No forms assigned</h3>
        <p class="text-gray-400 max-w-sm mx-auto">There are no questionnaires or data collection forms assigned to this project yet.</p>
      </div>

      <div v-else class="space-y-4">
        <div v-for="form in forms" :key="form.id" class="bg-layer-1 rounded-2xl border border-white/5 p-6 hover:bg-layer-2 transition-colors group flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-layer-2 text-accent rounded-xl flex items-center justify-center shrink-0 border border-white/10">
              <span class="material-symbols-outlined">receipt_long</span>
            </div>
            <div>
              <h3 class="font-bold text-white text-lg group-hover:text-accent transition-colors font-heading">{{ form.title }}</h3>
              <div class="flex items-center gap-4 mt-2">
                <span class="inline-flex items-center text-xs font-medium text-gray-500 font-mono">
                  <Clock class="w-3.5 h-3.5 mr-1 text-gray-500" />
                  Assigned: {{ new Date(form.created_at).toLocaleDateString() }}
                </span>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold font-mono tracking-wider uppercase border"
                      :class="{
                        'bg-white/5 text-gray-400 border-white/10': form.status === 'pending',
                        'bg-blue-900/30 text-blue-400 border-blue-900/50': form.status === 'partial',
                        'bg-accent/20 text-accent border-accent/20': form.status === 'completed'
                      }">
                  {{ form.status }}
                </span>
              </div>
            </div>
          </div>
          
          <NuxtLink :to="`/portal/${route.params.token}/forms/${form.id}`" class="px-5 py-2.5 text-sm font-bold text-layer-0 bg-accent rounded-lg hover:bg-[#a4d64c] transition-colors shrink-0 flex items-center justify-center">
            Open Form
          </NuxtLink>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, FileBox, Clock, FileText } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

definePageMeta({
  layout: 'portal'
})

const route = useRoute()
const projectId = route.params.id
const api = useApi()

const activeTab = ref('overview')

const project = ref(null)
const isLoadingProject = ref(true)
const error = ref(null)

const milestones = ref([])
const isLoadingMilestones = ref(true)

const deliverables = ref([])
const isLoadingDeliverables = ref(true)

const forms = ref([])
const isLoadingForms = ref(true)

const fetchProjectData = async () => {
  try {
    // Fetch project metadata
    project.value = await api(`/api/v1/portal/projects/${projectId}`)
    
    // Fetch milestones
    milestones.value = await api(`/api/v1/portal/projects/${projectId}/milestones`)
    
    // Fetch deliverables
    deliverables.value = await api(`/api/v1/portal/projects/${projectId}/deliverables`)
    
    // Fetch all forms and filter by project
    const allForms = await api('/api/v1/portal/forms')
    forms.value = allForms.filter(f => f.project_id === projectId)
  } catch (err) {
    console.error('Failed to fetch project details', err)
    error.value = 'Could not load project. It may have been deleted.'
  } finally {
    isLoadingProject.value = false
    isLoadingMilestones.value = false
    isLoadingDeliverables.value = false
    isLoadingForms.value = false
  }
}

onMounted(() => {
  if (route.query.tab) {
    activeTab.value = route.query.tab
  }
  fetchProjectData()
})
</script>
