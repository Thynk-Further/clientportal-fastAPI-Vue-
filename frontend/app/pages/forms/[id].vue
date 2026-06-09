<template>
  <div class="space-y-8 font-sans max-w-5xl mx-auto text-[#e3e2e2]">
    <!-- Navigation Back -->
    <div>
      <NuxtLink to="/forms" class="text-xs font-mono uppercase tracking-widest text-gray-500 hover:text-[#bef264] transition-colors flex items-center gap-1 w-fit">
        <span class="material-symbols-outlined text-sm">arrow_back</span>
        Back to Templates
      </NuxtLink>
    </div>

    <div v-if="isLoading" class="flex justify-center p-20">
      <span class="material-symbols-outlined animate-spin text-4xl text-[#bef264]">progress_activity</span>
    </div>

    <div v-else-if="template" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- LEFT: Form Builder Workspace -->
      <div class="lg:col-span-8 space-y-6">
        <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden">
          <div class="p-6 border-b border-white/5 bg-[#181818]/60">
            <h2 class="font-display text-2xl font-bold text-white mb-2">{{ template.name }}</h2>
            <p class="text-sm text-gray-400">{{ template.description || 'No description provided.' }}</p>
          </div>

          <div class="p-6 space-y-8 min-h-[400px]">
            <div v-if="fields.length === 0" class="text-center py-12 opacity-50">
              <span class="material-symbols-outlined text-4xl mb-2">post_add</span>
              <p class="text-sm">This template is empty.</p>
              <p class="text-xs font-mono mt-1 text-gray-400">Add fields from the right panel.</p>
            </div>

            <!-- Fields List (Builder mode) -->
            <div
              v-for="(field, index) in fields"
              :key="index"
              class="group relative border border-white/5 bg-[#1e2020]/50 rounded-xl p-5 hover:border-white/10 transition-colors"
            >
              <!-- Field Drag Handle & Controls -->
              <div class="absolute right-3 top-3 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 bg-[#171717] border border-white/10 rounded-md p-1 z-10 shadow-lg">
                <button @click="moveFieldUp(index)" :disabled="index === 0" class="p-1 hover:text-[#bef264] text-gray-400 disabled:opacity-30 disabled:cursor-not-allowed leading-none">
                  <span class="material-symbols-outlined text-sm">arrow_upward</span>
                </button>
                <button @click="moveFieldDown(index)" :disabled="index === fields.length - 1" class="p-1 hover:text-[#bef264] text-gray-400 disabled:opacity-30 disabled:cursor-not-allowed leading-none">
                  <span class="material-symbols-outlined text-sm">arrow_downward</span>
                </button>
                <div class="w-px h-4 bg-white/10 mx-1"></div>
                <button @click="removeField(index)" class="p-1 hover:text-red-400 text-gray-400 leading-none">
                  <span class="material-symbols-outlined text-sm">delete</span>
                </button>
              </div>

              <div class="space-y-4">
                <div class="flex items-start gap-4">
                  <!-- Type Icon -->
                  <div class="h-8 w-8 rounded bg-white/5 flex items-center justify-center shrink-0 border border-white/5 text-gray-400 mt-1">
                    <span v-if="field.field_type === 'text'" class="material-symbols-outlined text-sm">short_text</span>
                    <span v-else-if="field.field_type === 'long_text'" class="material-symbols-outlined text-sm">notes</span>
                    <span v-else-if="field.field_type === 'file_upload'" class="material-symbols-outlined text-sm">cloud_upload</span>
                  </div>

                  <div class="flex-1 space-y-3">
                    <input
                      v-model="field.label"
                      type="text"
                      placeholder="Question Label..."
                      class="w-full bg-transparent border-b border-white/10 text-white font-bold text-base focus:outline-none focus:border-[#bef264] transition-colors pb-1 placeholder:font-normal"
                    />
                    
                    <input
                      v-model="field.helper_text"
                      type="text"
                      placeholder="Helper text (optional)..."
                      class="w-full bg-transparent text-gray-400 text-xs focus:outline-none focus:text-white transition-colors"
                    />

                    <!-- Mock Input UI based on type -->
                    <div class="pt-2 opacity-50 pointer-events-none">
                      <div v-if="field.field_type === 'text'" class="w-full h-10 bg-black/20 rounded border border-white/5"></div>
                      <div v-else-if="field.field_type === 'long_text'" class="w-full h-20 bg-black/20 rounded border border-white/5"></div>
                      <div v-else-if="field.field_type === 'file_upload'" class="w-full h-16 bg-black/20 rounded border border-white/5 border-dashed flex items-center justify-center text-xs font-mono">Upload zone</div>
                    </div>
                  </div>
                </div>

                <div class="flex items-center justify-end gap-2 border-t border-white/5 pt-3 mt-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <span class="text-xs font-mono uppercase tracking-wider text-gray-400 select-none">Required</span>
                    <input type="checkbox" v-model="field.is_required" class="accent-[#bef264] w-3.5 h-3.5 cursor-pointer" />
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Toolbox & Actions -->
      <div class="lg:col-span-4 space-y-6 lg:sticky lg:top-6">
        
        <!-- Save Actions -->
        <div class="bg-[#171717] border border-[#bef264]/20 rounded-xl p-5 shadow-[0_0_15px_rgba(190,242,100,0.05)]">
          <button
            @click="saveTemplateFields"
            :disabled="isSaving"
            class="w-full bg-[#bef264] text-[#131f00] hover:bg-[#bef264]/80 font-bold py-3.5 rounded-lg text-sm transition-all duration-200 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider disabled:opacity-50 mb-3"
          >
            <span v-if="isSaving" class="material-symbols-outlined animate-spin text-lg">progress_activity</span>
            <span v-else class="material-symbols-outlined text-lg">save</span>
            Save Form Schema
          </button>
          
          <button
            @click="showAssignModal = true"
            :disabled="isSaving || fields.length === 0"
            class="w-full bg-[#1e2020] text-gray-300 border border-white/10 hover:border-[#bef264]/50 hover:text-white font-bold py-3 rounded-lg text-xs transition-all duration-200 cursor-pointer flex items-center justify-center gap-2 font-mono uppercase tracking-wider disabled:opacity-50"
          >
            <span class="material-symbols-outlined text-sm">send</span>
            Deploy to Project
          </button>
        </div>

        <!-- Add Fields Toolbox -->
        <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden">
          <div class="p-4 border-b border-white/5 bg-[#181818]/60">
            <h3 class="font-bold text-white text-xs font-mono uppercase tracking-wider">Field Toolbox</h3>
          </div>
          <div class="p-4 space-y-2">
            <button @click="addField('text')" class="w-full flex items-center gap-3 p-3 rounded-lg bg-[#1e2020] border border-white/5 hover:border-[#bef264]/30 hover:bg-[#bef264]/5 text-left transition-colors text-white cursor-pointer group">
              <span class="material-symbols-outlined text-gray-400 group-hover:text-[#bef264]">short_text</span>
              <div>
                <div class="text-sm font-bold">Short Answer</div>
                <div class="text-[10px] text-gray-500 font-mono">Single line text input</div>
              </div>
            </button>
            
            <button @click="addField('long_text')" class="w-full flex items-center gap-3 p-3 rounded-lg bg-[#1e2020] border border-white/5 hover:border-[#bef264]/30 hover:bg-[#bef264]/5 text-left transition-colors text-white cursor-pointer group">
              <span class="material-symbols-outlined text-gray-400 group-hover:text-[#bef264]">notes</span>
              <div>
                <div class="text-sm font-bold">Paragraph</div>
                <div class="text-[10px] text-gray-500 font-mono">Multi-line text area</div>
              </div>
            </button>

            <button @click="addField('file_upload')" class="w-full flex items-center gap-3 p-3 rounded-lg bg-[#1e2020] border border-white/5 hover:border-[#bef264]/30 hover:bg-[#bef264]/5 text-left transition-colors text-white cursor-pointer group">
              <span class="material-symbols-outlined text-gray-400 group-hover:text-[#bef264]">cloud_upload</span>
              <div>
                <div class="text-sm font-bold">File Upload</div>
                <div class="text-[10px] text-gray-500 font-mono">Direct-to-R2 bypass</div>
              </div>
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- ASSIGN MODAL -->
    <div v-if="showAssignModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-8 max-w-md w-full space-y-6">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-xl font-bold text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-[#bef264]">send</span>
            Deploy Form Assignment
          </h4>
          <button
            @click="showAssignModal = false"
            class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer transition-colors"
          >
            close
          </button>
        </div>

        <p class="text-xs text-gray-400">
          This will assign the form to a specific project. An email notification will be dispatched to the client with a link to complete it securely in their portal.
        </p>

        <form @submit.prevent="assignForm" class="space-y-4 font-sans text-sm mt-4">
          <div v-if="assignError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
            {{ assignError }}
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Display Title</label>
            <input
              v-model="assignFormModel.title"
              type="text"
              required
              placeholder="e.g. Website Questionnaire"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isAssigning"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Target Project</label>
            <select
              v-model="assignFormModel.project_id"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none appearance-none"
              :disabled="isAssigning"
            >
              <option value="" disabled>Select a project...</option>
              <option v-for="p in projects" :key="p.id" :value="p.id">
                {{ p.name }}
              </option>
            </select>
          </div>

          <div class="flex justify-end gap-2 text-sm pt-4">
            <button
              type="button"
              @click="showAssignModal = false"
              :disabled="isAssigning"
              class="px-5 py-2.5 rounded-lg hover:bg-white/[0.05] transition-colors disabled:opacity-50 text-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isAssigning || !assignFormModel.project_id"
              class="px-6 py-2.5 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg cursor-pointer transform active:scale-95 transition-all text-xs uppercase font-mono tracking-wider disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="isAssigning" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              Deploy Now
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from '#app'
import { useApi } from '~/composables/useApi'

const api = useApi()
const route = useRoute()
const router = useRouter()

const template = ref(null)
const fields = ref([])
const isLoading = ref(true)
const isSaving = ref(false)

const templateId = route.params.id

// Assignment States
const showAssignModal = ref(false)
const isAssigning = ref(false)
const assignError = ref('')
const projects = ref([])
const assignFormModel = ref({
  title: '',
  project_id: ''
})

const fetchTemplate = async () => {
  try {
    const data = await api(`/api/v1/form-templates/${templateId}`)
    template.value = data
    assignFormModel.value.title = data.name
    // Copy existing fields
    fields.value = data.fields ? JSON.parse(JSON.stringify(data.fields)) : []
  } catch (err) {
    console.error('Failed to fetch template', err)
    router.push('/forms')
  } finally {
    isLoading.value = false
  }
}

const fetchProjects = async () => {
  try {
    projects.value = await api('/api/v1/projects')
  } catch (err) {
    console.error('Failed to fetch projects', err)
  }
}

const addField = (type) => {
  fields.value.push({
    label: '',
    helper_text: '',
    field_type: type,
    is_required: false,
    options: null,
    sort_order: fields.value.length
  })
}

const removeField = (index) => {
  fields.value.splice(index, 1)
}

const moveFieldUp = (index) => {
  if (index === 0) return
  const temp = fields.value[index]
  fields.value[index] = fields.value[index - 1]
  fields.value[index - 1] = temp
}

const moveFieldDown = (index) => {
  if (index === fields.value.length - 1) return
  const temp = fields.value[index]
  fields.value[index] = fields.value[index + 1]
  fields.value[index + 1] = temp
}

const saveTemplateFields = async () => {
  isSaving.value = true
  
  // Re-apply sort_order based on array index
  const payload = fields.value.map((f, i) => ({
    label: f.label || 'Untitled Question',
    helper_text: f.helper_text || null,
    field_type: f.field_type,
    is_required: f.is_required,
    options: f.options,
    sort_order: i
  }))

  try {
    const updatedFields = await api(`/api/v1/form-templates/${templateId}/fields`, {
      method: 'POST',
      body: payload
    })
    fields.value = updatedFields
    alert('Form schema saved successfully!')
  } catch (err) {
    alert(err.data?.detail || 'Failed to save schema.')
  } finally {
    isSaving.value = false
  }
}

const assignForm = async () => {
  assignError.value = ''
  isAssigning.value = true
  
  // Auto-save the schema before assigning
  await saveTemplateFields()

  try {
    await api(`/api/v1/projects/${assignFormModel.value.project_id}/forms`, {
      method: 'POST',
      body: {
        form_template_id: templateId,
        title: assignFormModel.value.title
      }
    })
    showAssignModal.value = false
    alert('Form successfully deployed! The client has been notified.')
    router.push('/forms')
  } catch (err) {
    assignError.value = err.data?.detail || 'Failed to assign form.'
  } finally {
    isAssigning.value = false
  }
}

onMounted(() => {
  fetchTemplate()
  fetchProjects()
})
</script>
