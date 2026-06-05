<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    <!-- Header -->
    <section class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
          Forms & Questionnaires
        </h2>
        <p class="text-xs text-gray-400 mt-2">
          Design data-collection templates, assign them to clients, and manage submissions.
        </p>
      </div>
      <div class="flex gap-2">
        <button
          @click="showCreateModal = true"
          class="bg-[#bef264] text-[#131f00] hover:bg-[#bef264]/80 font-bold px-5 py-3 rounded-lg text-sm transition-all duration-100 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider"
        >
          <span class="material-symbols-outlined text-md">post_add</span>
          Create Template
        </button>
      </div>
    </section>

    <!-- Navigation Tabs -->
    <div class="flex border-b border-white/5 space-x-6">
      <button
        @click="activeTab = 'templates'"
        :class="`pb-3 text-xs font-mono uppercase tracking-widest font-bold transition-colors border-b-2 ${
          activeTab === 'templates' ? 'text-[#bef264] border-[#bef264]' : 'text-gray-500 border-transparent hover:text-white'
        }`"
      >
        Form Templates
      </button>
      <button
        @click="activeTab = 'submissions'"
        :class="`pb-3 text-xs font-mono uppercase tracking-widest font-bold transition-colors border-b-2 ${
          activeTab === 'submissions' ? 'text-[#bef264] border-[#bef264]' : 'text-gray-500 border-transparent hover:text-white'
        }`"
      >
        Active Assignments
      </button>
    </div>

    <!-- TAB: Templates -->
    <div v-if="activeTab === 'templates'" class="space-y-6">
      <div v-if="isLoadingTemplates" class="flex justify-center p-12">
        <span class="material-symbols-outlined animate-spin text-3xl text-[#bef264]/50">progress_activity</span>
      </div>

      <div v-else-if="templates.length === 0" class="text-center py-20 bg-[#171717] border border-white/[0.08] rounded-xl opacity-80">
        <span class="material-symbols-outlined text-5xl text-gray-400/40 mb-3 animate-pulse">
          receipt_long
        </span>
        <h3 class="text-lg font-bold text-white mb-1">No Templates Designed</h3>
        <p class="text-gray-400 font-mono text-xs max-w-md mx-auto mb-6">Create your first form template to start collecting structured data and assets from your clients.</p>
        <button
          @click="showCreateModal = true"
          class="px-4 py-2 border border-[#bef264] text-[#bef264] rounded hover:bg-[#bef264] hover:text-[#131f00] font-mono text-xs uppercase tracking-wider font-bold transition-colors cursor-pointer"
        >
          Build a template
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="t in templates"
          :key="t.id"
          class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden hover:border-[#bef264]/20 transition-all group flex flex-col h-full cursor-pointer"
          @click="$router.push(`/forms/${t.id}`)"
        >
          <div class="h-1 bg-gradient-to-r from-blue-500/20 to-transparent group-hover:from-[#bef264]/20 transition-all"></div>
          
          <div class="p-6 flex-1 flex flex-col">
            <div class="flex justify-between items-start mb-4">
              <div class="h-10 w-10 rounded-lg bg-[#1e2020] border border-white/5 flex items-center justify-center text-[#bef264]">
                <span class="material-symbols-outlined text-lg">description</span>
              </div>
            </div>
            
            <h3 class="font-bold text-white text-lg mb-1 group-hover:text-[#bef264] transition-colors">{{ t.name }}</h3>
            <p class="text-xs text-gray-400 line-clamp-2 mb-4 flex-1">{{ t.description || 'No description provided.' }}</p>
            
            <div class="flex items-center gap-4 text-xs font-mono text-gray-500 border-t border-white/5 pt-4 mt-auto">
              <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-[14px]">format_list_bulleted</span> {{ t.fields?.length || 0 }} Fields</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB: Submissions -->
    <div v-if="activeTab === 'submissions'" class="space-y-6">
      <div v-if="isLoadingSubmissions" class="flex justify-center p-12">
        <span class="material-symbols-outlined animate-spin text-3xl text-[#bef264]/50">progress_activity</span>
      </div>

      <div v-else-if="submissions.length === 0" class="text-center py-20 bg-[#171717] border border-white/[0.08] rounded-xl opacity-80">
        <span class="material-symbols-outlined text-5xl text-gray-400/40 mb-3 animate-pulse">
          forward_to_inbox
        </span>
        <h3 class="text-lg font-bold text-white mb-1">No Active Assignments</h3>
        <p class="text-gray-400 font-mono text-xs max-w-md mx-auto">Deploy a form template to a project to start tracking client responses.</p>
      </div>

      <div v-else class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden overflow-x-auto">
        <table class="w-full text-left text-sm whitespace-nowrap">
          <thead class="bg-white/[0.02] border-b border-white/[0.05] font-mono text-[10px] uppercase tracking-wider text-gray-500">
            <tr>
              <th class="px-5 py-3">Form Context</th>
              <th class="px-5 py-3">Deployed To</th>
              <th class="px-5 py-3 text-center">Status</th>
              <th class="px-5 py-3 text-right">Responses</th>
              <th class="px-5 py-3"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.05] font-sans">
            <tr v-for="sub in submissions" :key="sub.id" class="hover:bg-white/[0.01] transition-colors group">
              <td class="px-5 py-4">
                <div class="font-bold text-white">{{ sub.title }}</div>
                <div class="text-[10px] text-gray-500 font-mono mt-0.5">Assigned: {{ new Date(sub.created_at).toLocaleDateString() }}</div>
              </td>
              <td class="px-5 py-4">
                <div class="text-xs text-gray-300 font-mono">Project ID:</div>
                <div class="text-[10px] text-gray-500 font-mono truncate max-w-[150px]">{{ sub.project_id }}</div>
              </td>
              <td class="px-5 py-4 text-center">
                <span :class="`px-2 py-1 rounded text-[9px] font-bold border uppercase tracking-wider ${
                  sub.status === 'completed' ? 'bg-green-500/10 text-green-400 border-green-500/20' :
                  sub.status === 'partial' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
                  'bg-white/5 text-gray-400 border-white/10'
                }`">
                  {{ sub.status }}
                </span>
              </td>
              <td class="px-5 py-4 text-right font-mono text-xs text-white">
                {{ sub.responses?.length || 0 }} fields
              </td>
              <td class="px-5 py-4 text-right">
                <button
                  class="px-3 py-1.5 bg-[#1e2020] hover:bg-[#bef264] hover:text-[#131f00] text-gray-300 text-[10px] font-bold font-mono rounded border border-white/5 transition-colors cursor-pointer uppercase"
                >
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL: Create Template -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-8 max-w-md w-full space-y-6">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-xl font-bold text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-[#bef264]">post_add</span>
            New Form Template
          </h4>
          <button
            @click="showCreateModal = false"
            class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer transition-colors"
          >
            close
          </button>
        </div>

        <form @submit.prevent="createTemplate" class="space-y-4 font-sans text-sm">
          <div v-if="createError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
            {{ createError }}
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Template Name</label>
            <input
              v-model="createForm.name"
              type="text"
              required
              placeholder="e.g. Website Onboarding Questionnaire"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isCreating"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Description (Optional)</label>
            <textarea
              v-model="createForm.description"
              rows="3"
              placeholder="Briefly describe what this form is used for..."
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none resize-none"
              :disabled="isCreating"
            ></textarea>
          </div>

          <div class="flex justify-end gap-2 text-sm pt-4">
            <button
              type="button"
              @click="showCreateModal = false"
              :disabled="isCreating"
              class="px-5 py-2.5 rounded-lg hover:bg-white/[0.05] transition-colors disabled:opacity-50 text-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isCreating"
              class="px-6 py-2.5 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg cursor-pointer transform active:scale-95 transition-all text-xs uppercase font-mono tracking-wider disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="isCreating" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              Save Template
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from '#app'
import { useApi } from '~/composables/useApi'

const api = useApi()
const router = useRouter()

const activeTab = ref('templates')

// Data states
const templates = ref([])
const submissions = ref([])
const isLoadingTemplates = ref(true)
const isLoadingSubmissions = ref(true)

// Modal states
const showCreateModal = ref(false)
const isCreating = ref(false)
const createError = ref('')
const createForm = ref({
  name: '',
  description: ''
})

const fetchTemplates = async () => {
  try {
    templates.value = await api('/api/v1/form-templates')
  } catch (err) {
    console.error('Failed to fetch templates', err)
  } finally {
    isLoadingTemplates.value = false
  }
}

const fetchSubmissions = async () => {
  try {
    submissions.value = await api('/api/v1/form-submissions')
  } catch (err) {
    console.error('Failed to fetch submissions', err)
  } finally {
    isLoadingSubmissions.value = false
  }
}

const createTemplate = async () => {
  createError.value = ''
  isCreating.value = true
  try {
    const newTemplate = await api('/api/v1/form-templates', {
      method: 'POST',
      body: {
        name: createForm.value.name,
        description: createForm.value.description || null
      }
    })
    showCreateModal.value = false
    // Route to builder
    router.push(`/forms/${newTemplate.id}`)
  } catch (err) {
    createError.value = err.data?.detail || 'Failed to create template.'
    isCreating.value = false
  }
}

onMounted(() => {
  fetchTemplates()
  fetchSubmissions()
})
</script>
