<template>
  <div class="max-w-3xl mx-auto space-y-8 pb-12">
    <!-- Back Navigation -->
    <div class="mb-8">
      <NuxtLink :to="`/portal/${route.params.token}`" class="text-xs font-mono uppercase tracking-widest text-gray-500 hover:text-white transition-colors flex items-center gap-1 w-fit">
        <span class="material-symbols-outlined text-sm">arrow_back</span>
        Back to Portal
      </NuxtLink>
    </div>

    <div v-if="isLoading" class="flex justify-center p-20">
      <span class="material-symbols-outlined animate-spin text-4xl text-brand-primary">progress_activity</span>
    </div>

    <div v-else-if="submission && template" class="space-y-8">
      
      <!-- Header -->
      <div class="bg-[#171717] border border-white/5 rounded-2xl p-8">
        <div class="flex items-center gap-3 mb-4">
          <span class="material-symbols-outlined text-brand-primary text-3xl">dynamic_form</span>
          <span v-if="submission.status === 'completed'" class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest rounded bg-green-500/10 text-green-400 border border-green-500/20">Completed</span>
          <span v-else-if="submission.status === 'partial'" class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">Draft Saved</span>
          <span v-else class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest rounded bg-white/5 text-gray-400 border border-white/10">To Do</span>
        </div>
        
        <h1 class="font-display text-3xl font-bold text-white mb-2">{{ submission.title }}</h1>
        <p class="text-gray-400 text-sm">{{ template.description }}</p>
      </div>

      <div v-if="submission.status === 'completed'" class="bg-green-500/10 border border-green-500/20 rounded-xl p-6 text-center">
        <span class="material-symbols-outlined text-green-400 text-5xl mb-2">task_alt</span>
        <h3 class="text-white font-bold text-lg mb-1">Form Submitted</h3>
        <p class="text-gray-400 text-sm">Thank you! Your responses have been saved and sent to the freelancer.</p>
      </div>

      <!-- Form Fields List -->
      <form v-else @submit.prevent="submitForm" class="space-y-6">
        
        <div
          v-for="field in template.fields"
          :key="field.id"
          class="bg-[#171717] border border-white/5 rounded-xl p-6 hover:border-white/10 transition-colors"
        >
          <div class="mb-4">
            <label class="block text-white font-bold text-base">
              {{ field.label }}
              <span v-if="field.is_required" class="text-red-400 ml-1" title="Required">*</span>
            </label>
            <p v-if="field.helper_text" class="text-gray-500 text-xs mt-1">{{ field.helper_text }}</p>
          </div>

          <!-- Type: Short Text -->
          <input
            v-if="field.field_type === 'text'"
            v-model="responses[field.id].value_text"
            type="text"
            :required="field.is_required"
            class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-brand-primary outline-none transition-all placeholder:text-gray-600"
            placeholder="Type your answer here..."
            @input="debouncedAutoSave"
          />

          <!-- Type: Long Text -->
          <textarea
            v-else-if="field.field_type === 'long_text'"
            v-model="responses[field.id].value_text"
            :required="field.is_required"
            rows="4"
            class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-brand-primary outline-none transition-all resize-y placeholder:text-gray-600"
            placeholder="Type your answer here..."
            @input="debouncedAutoSave"
          ></textarea>

          <!-- Type: File Upload -->
          <div v-else-if="field.field_type === 'file_upload'">
            <!-- If file already uploaded -->
            <div v-if="responses[field.id].value_file_object_key" class="flex items-center justify-between bg-brand-primary/5 border border-brand-primary/20 rounded-lg p-4">
              <div class="flex items-center gap-3 min-w-0">
                <span class="material-symbols-outlined text-brand-primary text-2xl shrink-0">check_circle</span>
                <div class="truncate">
                  <div class="text-sm font-bold text-white truncate">File Attached</div>
                  <div class="text-[10px] text-brand-primary font-mono truncate">Ready for submission</div>
                </div>
              </div>
              <button type="button" @click="removeFile(field.id)" class="text-gray-400 hover:text-red-400 p-2 cursor-pointer transition-colors">
                <span class="material-symbols-outlined text-sm">delete</span>
              </button>
            </div>
            
            <!-- Upload area -->
            <div v-else class="relative">
              <input
                type="file"
                :id="`file-${field.id}`"
                class="hidden"
                @change="(e) => handleFileUpload(e, field.id)"
              />
              <label
                :for="`file-${field.id}`"
                :class="`w-full border-2 border-dashed rounded-lg p-8 flex flex-col items-center justify-center cursor-pointer transition-all ${
                  uploadProgress[field.id] ? 'border-brand-primary bg-brand-primary/5' : 'border-white/10 hover:border-brand-primary/50 hover:bg-[#1e2020]'
                }`"
              >
                <div v-if="uploadProgress[field.id]" class="text-center">
                  <span class="material-symbols-outlined animate-spin text-3xl text-brand-primary mb-2">progress_activity</span>
                  <div class="text-sm font-bold text-white text-brand-primary">Uploading {{ uploadProgress[field.id] }}%</div>
                </div>
                <div v-else class="text-center">
                  <span class="material-symbols-outlined text-3xl text-gray-400 mb-2">cloud_upload</span>
                  <div class="text-sm font-bold text-white">Click to select a file</div>
                  <div class="text-xs text-gray-500 mt-1">Direct secure upload</div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Sticky Actions Bar -->
        <div class="sticky bottom-6 bg-[#171717]/90 backdrop-blur-md border border-white/10 rounded-2xl p-4 shadow-2xl flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span v-if="isSaving" class="text-[10px] font-mono text-gray-400 flex items-center gap-1 uppercase tracking-wider">
              <span class="material-symbols-outlined animate-spin text-sm">sync</span> Saving draft...
            </span>
            <span v-else-if="lastSavedAt" class="text-[10px] font-mono text-green-400 flex items-center gap-1 uppercase tracking-wider">
              <span class="material-symbols-outlined text-sm">cloud_done</span> Saved {{ lastSavedAt }}
            </span>
          </div>

          <div class="flex gap-3">
            <button
              type="button"
              @click="triggerAutoSave"
              :disabled="isSaving"
              class="px-5 py-3 rounded-lg border border-white/10 hover:bg-white/5 font-bold text-white text-sm transition-colors cursor-pointer disabled:opacity-50"
            >
              Save Draft
            </button>
            <button
              type="submit"
              :disabled="isSubmitting || isSaving"
              class="px-8 py-3 rounded-lg font-bold text-sm transition-all cursor-pointer bg-brand-primary text-[#131f00] hover:bg-brand-primary/80 active:scale-95 disabled:opacity-50 flex items-center gap-2 font-mono uppercase tracking-wider shadow-[0_0_20px_rgba(var(--color-brand-primary),0.3)]"
            >
              <span v-if="isSubmitting" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              <span v-else class="material-symbols-outlined text-sm">send</span>
              Submit Final
            </button>
          </div>
        </div>
      </form>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from '#app'
import { useApi } from '~/composables/useApi'

// Use portal layout which automatically extracts branding
definePageMeta({
  layout: 'portal'
})

const route = useRoute()
const api = useApi()

const submissionId = route.params.id
const submission = ref(null)
const template = ref(null)
const isLoading = ref(true)

// Reactive form state: key = field_id, value = { value_text, value_file_object_key }
const responses = ref({})

// Saving states
const isSaving = ref(false)
const isSubmitting = ref(false)
const lastSavedAt = ref('')
let saveTimeout = null

// File Upload state
const uploadProgress = ref({}) // key = field_id, value = percentage 0-100

const fetchForm = async () => {
  try {
    const data = await api(`/api/v1/portal/forms/${submissionId}`)
    submission.value = data.submission
    template.value = data.template

    // Initialize responses map
    template.value.fields.forEach(field => {
      // Find if we have an existing response
      const existing = submission.value.responses.find(r => r.form_field_id === field.id)
      responses.value[field.id] = {
        value_text: existing?.value_text || '',
        value_file_object_key: existing?.value_file_object_key || null
      }
    })
  } catch (err) {
    console.error('Failed to load form', err)
    alert('Form not found or you do not have access.')
  } finally {
    isLoading.value = false
  }
}

// Auto-save logic
const triggerAutoSave = async () => {
  if (submission.value?.status === 'completed') return
  
  isSaving.value = true
  try {
    // Format payload
    const payload = []
    Object.keys(responses.value).forEach(fieldId => {
      const resp = responses.value[fieldId]
      if (resp.value_text || resp.value_file_object_key) {
        payload.push({
          form_field_id: fieldId,
          value_text: resp.value_text || null,
          value_file_object_key: resp.value_file_object_key || null
        })
      }
    })

    if (payload.length > 0) {
      await api(`/api/v1/portal/forms/${submissionId}/responses`, {
        method: 'POST',
        body: { responses: payload }
      })
      lastSavedAt.value = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      submission.value.status = 'partial'
    }
  } catch (err) {
    console.error('Auto-save failed', err)
  } finally {
    isSaving.value = false
  }
}

const debouncedAutoSave = () => {
  if (saveTimeout) clearTimeout(saveTimeout)
  saveTimeout = setTimeout(() => {
    triggerAutoSave()
  }, 1500) // save 1.5s after user stops typing
}

const handleFileUpload = async (event, fieldId) => {
  const file = event.target.files[0]
  if (!file) return

  uploadProgress.value[fieldId] = 1

  try {
    // 1. Get presigned URL
    const { presigned_url, object_key } = await api(`/api/v1/portal/forms/${submissionId}/fields/${fieldId}/presigned-url`, {
      method: 'POST',
      body: {
        filename: file.name,
        content_type: file.type || 'application/octet-stream'
      }
    })

    // 2. Upload directly to R2 using XMLHttpRequest to track progress
    await new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('PUT', presigned_url, true)
      xhr.setRequestHeader('Content-Type', file.type || 'application/octet-stream')
      
      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          uploadProgress.value[fieldId] = Math.round((e.loaded / e.total) * 100)
        }
      }
      
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) resolve()
        else reject(new Error('Upload failed'))
      }
      xhr.onerror = () => reject(new Error('Network error during upload'))
      
      xhr.send(file)
    })

    // 3. Save the response
    responses.value[fieldId].value_file_object_key = object_key
    await triggerAutoSave()

  } catch (err) {
    console.error('File upload failed', err)
    alert('Failed to upload file. Please try again.')
  } finally {
    uploadProgress.value[fieldId] = null
    event.target.value = '' // reset input
  }
}

const removeFile = async (fieldId) => {
  responses.value[fieldId].value_file_object_key = null
  await triggerAutoSave()
}

const submitForm = async () => {
  // Save any pending drafts first
  await triggerAutoSave()
  
  isSubmitting.value = true
  try {
    await api(`/api/v1/portal/forms/${submissionId}/submit`, {
      method: 'POST'
    })
    submission.value.status = 'completed'
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (err) {
    alert(err.data?.detail || 'Failed to submit form. Make sure all required fields are filled.')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchForm()
})

onUnmounted(() => {
  if (saveTimeout) clearTimeout(saveTimeout)
})
</script>
