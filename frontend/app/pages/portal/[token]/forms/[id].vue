<template>
  <div class="space-y-6 max-w-4xl mx-auto pb-24">
    
    <!-- Back Navigation -->
    <div class="flex items-center gap-2 mb-4">
      <NuxtLink :to="`/portal/${route.params.token}/projects/${submission?.project_id || ''}`" class="inline-flex items-center text-sm font-medium text-gray-400 hover:text-white transition-colors">
        <span class="material-symbols-outlined text-sm mr-1">arrow_back</span>
        Back to Project
      </NuxtLink>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="animate-pulse space-y-6">
      <div class="h-40 bg-layer-1 rounded-3xl border border-white/5"></div>
      <div class="space-y-4">
        <div v-for="i in 3" :key="i" class="h-32 bg-layer-1 rounded-2xl border border-white/5"></div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-900/20 p-6 rounded-2xl border border-red-900/50 text-center">
      <p class="text-red-400">{{ error }}</p>
    </div>

    <template v-else>
      <!-- Form Header -->
      <div class="bg-layer-1 rounded-3xl border border-white/5 p-8 shadow-sm relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-accent rounded-full blur-[80px] opacity-20 pointer-events-none"></div>

        <div class="relative z-10 flex flex-col md:flex-row justify-between gap-6">
          <div>
            <h1 class="text-3xl font-bold text-white tracking-tight font-heading mb-2">{{ submission.title }}</h1>
            <p class="text-lg text-gray-400 max-w-3xl">{{ template.description || 'Please complete the questionnaire below.' }}</p>
          </div>
          <div class="shrink-0 flex items-start">
             <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold font-mono tracking-wider uppercase border"
                  :class="{
                    'bg-white/5 text-gray-400 border-white/10': submission.status === 'pending',
                    'bg-blue-900/30 text-blue-400 border-blue-900/50': submission.status === 'partial',
                    'bg-accent/20 text-accent border-accent/20': submission.status === 'completed'
                  }">
              {{ submission.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- Form Body -->
      <form @submit.prevent="submitForm" class="space-y-6">
        
        <div v-for="field in template.fields" :key="field.id" class="bg-layer-1 rounded-2xl border border-white/5 p-6 md:p-8">
          <label :for="field.id" class="block font-bold text-white text-lg font-heading mb-1">
            {{ field.label }}
            <span v-if="field.is_required" class="text-red-500 ml-1" title="Required">*</span>
          </label>
          <p v-if="field.helper_text" class="text-sm text-gray-400 mb-4">{{ field.helper_text }}</p>

          <!-- Input rendering based on type -->
          
          <!-- Short Text -->
          <input
            v-if="field.field_type === 'text'"
            :id="field.id"
            v-model="responses[field.id].value_text"
            type="text"
            class="w-full bg-layer-2 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-accent/50 transition-colors"
            placeholder="Type your answer here..."
            :disabled="isReadOnly"
            :required="field.is_required"
          />

          <!-- Long Text -->
          <textarea
            v-else-if="field.field_type === 'long_text'"
            :id="field.id"
            v-model="responses[field.id].value_text"
            rows="4"
            class="w-full bg-layer-2 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-accent/50 transition-colors resize-y min-h-[100px]"
            placeholder="Type your detailed answer here..."
            :disabled="isReadOnly"
            :required="field.is_required"
          ></textarea>

          <!-- File Upload -->
          <div v-else-if="field.field_type === 'file_upload'" class="space-y-3">
            <div v-if="responses[field.id].value_file_object_key" class="flex items-center gap-3 bg-layer-2 border border-white/10 p-4 rounded-xl relative overflow-hidden">
              <span class="material-symbols-outlined text-accent">check_circle</span>
              <div>
                <p class="text-sm text-white font-medium">File Uploaded Successfully</p>
                <p class="text-xs text-gray-400 font-mono mt-0.5 truncate max-w-sm">{{ responses[field.id].value_file_object_key.split('_').slice(1).join('_') || responses[field.id].value_file_object_key }}</p>
              </div>
              <button 
                v-if="!isReadOnly"
                type="button" 
                @click="responses[field.id].value_file_object_key = ''" 
                class="absolute right-4 top-1/2 -translate-y-1/2 p-2 hover:bg-white/5 rounded-full text-gray-400 hover:text-red-400 transition-colors"
              >
                <span class="material-symbols-outlined text-sm">delete</span>
              </button>
            </div>
            
            <div v-else class="relative group">
              <input
                type="file"
                :id="field.id"
                @change="e => handleFileUpload(e, field.id)"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed z-10"
                :disabled="isReadOnly || uploadingFieldId === field.id"
              />
              <div class="border-2 border-dashed border-white/10 group-hover:border-accent/30 rounded-xl p-8 flex flex-col items-center justify-center text-center transition-colors bg-layer-2 relative overflow-hidden"
                   :class="{'opacity-50': uploadingFieldId === field.id}">
                
                <!-- Loading Overlay -->
                <div v-if="uploadingFieldId === field.id" class="absolute inset-0 bg-layer-2/80 backdrop-blur-sm flex flex-col items-center justify-center z-20">
                  <span class="material-symbols-outlined animate-spin text-3xl text-accent mb-2">progress_activity</span>
                  <span class="text-xs font-mono uppercase tracking-widest text-accent font-bold">Uploading...</span>
                </div>

                <span class="material-symbols-outlined text-4xl text-gray-500 mb-3 group-hover:text-accent transition-colors">cloud_upload</span>
                <p class="text-sm font-medium text-white mb-1">Click or drag file to upload</p>
                <p class="text-xs text-gray-400 font-mono">Max size: 50MB</p>
              </div>
            </div>
            <!-- Hidden input for HTML validation if required -->
            <input type="text" class="w-0 h-0 opacity-0 absolute" :value="responses[field.id].value_file_object_key" :required="field.is_required && !responses[field.id].value_file_object_key" />
          </div>

        </div>

        <!-- Submit Actions -->
        <div v-if="!isReadOnly" class="bg-layer-1 border border-white/5 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-4 sticky bottom-6 z-30 shadow-2xl">
          <p class="text-xs text-gray-400 font-mono">
            Unsaved changes will be lost if you leave this page.
          </p>
          <div class="flex items-center gap-3 w-full md:w-auto">
            <button
              type="button"
              @click="saveDraft"
              :disabled="isSaving"
              class="flex-1 md:flex-none px-6 py-3 bg-layer-2 hover:bg-white/[0.05] text-white font-bold rounded-xl transition-all border border-white/5 text-sm disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <span v-if="isSaving && saveType === 'draft'" class="material-symbols-outlined animate-spin text-[18px]">progress_activity</span>
              Save Draft
            </button>
            <button
              type="submit"
              :disabled="isSaving"
              class="flex-1 md:flex-none px-8 py-3 bg-accent hover:bg-[#a4d64c] text-layer-0 font-bold rounded-xl transition-all text-sm disabled:opacity-50 flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(190,242,100,0.1)]"
            >
              <span v-if="isSaving && saveType === 'submit'" class="material-symbols-outlined animate-spin text-[18px]">progress_activity</span>
              <span v-else class="material-symbols-outlined text-[18px]">send</span>
              Final Submit
            </button>
          </div>
        </div>

      </form>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '~/composables/useApi'

definePageMeta({
  layout: 'portal'
})

const route = useRoute()
const api = useApi()

const isLoading = ref(true)
const error = ref(null)
const submission = ref(null)
const template = ref(null)

// Map of field_id -> response object
const responses = ref({})

const isSaving = ref(false)
const saveType = ref(null) // 'draft' or 'submit'
const uploadingFieldId = ref(null)

const submissionId = route.params.id

const isReadOnly = computed(() => {
  return submission.value?.status === 'completed'
})

const fetchForm = async () => {
  try {
    const data = await api(`/api/v1/portal/forms/${submissionId}`)
    submission.value = data.submission
    template.value = data.template

    // Initialize response map
    const responseMap = {}
    
    // Set default empty responses for all fields
    template.value.fields.forEach(field => {
      responseMap[field.id] = {
        form_field_id: field.id,
        value_text: '',
        value_file_object_key: ''
      }
    })

    // Populate with existing responses
    if (submission.value.responses) {
      submission.value.responses.forEach(res => {
        if (responseMap[res.form_field_id]) {
          responseMap[res.form_field_id].value_text = res.value_text || ''
          responseMap[res.form_field_id].value_file_object_key = res.value_file_object_key || ''
        }
      })
    }
    
    responses.value = responseMap
  } catch (err) {
    console.error('Failed to fetch form', err)
    error.value = 'Form could not be loaded or you do not have permission to view it.'
  } finally {
    isLoading.value = false
  }
}

const handleFileUpload = async (event, fieldId) => {
  const file = event.target.files[0]
  if (!file) return

  // Basic client-side validation
  if (file.size > 50 * 1024 * 1024) {
    alert('File size exceeds 50MB limit.')
    event.target.value = ''
    return
  }

  uploadingFieldId.value = fieldId
  
  try {
    // 1. Get presigned URL
    const { presigned_url, object_key } = await api(`/api/v1/portal/forms/${submissionId}/fields/${fieldId}/presigned-url`, {
      method: 'POST',
      body: {
        filename: file.name,
        content_type: file.type || 'application/octet-stream'
      }
    })

    // 2. Upload file directly to R2
    const uploadRes = await fetch(presigned_url, {
      method: 'PUT',
      headers: {
        'Content-Type': file.type || 'application/octet-stream'
      },
      body: file
    })

    if (!uploadRes.ok) {
      throw new Error(`Upload failed with status: ${uploadRes.status}`)
    }

    // 3. Save object key to responses map
    responses.value[fieldId].value_file_object_key = object_key
    
  } catch (err) {
    console.error('File upload failed:', err)
    alert('Failed to upload file. Please try again.')
  } finally {
    uploadingFieldId.value = null
    event.target.value = '' // Reset file input
  }
}

const buildResponsePayload = () => {
  return {
    responses: Object.values(responses.value).map(r => ({
      form_field_id: r.form_field_id,
      value_text: r.value_text.trim() || null,
      value_file_object_key: r.value_file_object_key || null
    })).filter(r => r.value_text !== null || r.value_file_object_key !== null)
  }
}

const saveDraft = async () => {
  if (isReadOnly.value) return
  isSaving.value = true
  saveType.value = 'draft'
  
  try {
    const payload = buildResponsePayload()
    await api(`/api/v1/portal/forms/${submissionId}/responses`, {
      method: 'POST',
      body: payload
    })
    
    submission.value.status = 'partial'
    alert('Draft saved successfully!')
  } catch (err) {
    console.error('Failed to save draft', err)
    alert(err.data?.detail || 'Failed to save draft.')
  } finally {
    isSaving.value = false
    saveType.value = null
  }
}

const submitForm = async () => {
  if (isReadOnly.value) return
  
  if (!confirm('Are you sure you want to submit? You will not be able to edit your answers after submitting.')) {
    return
  }
  
  isSaving.value = true
  saveType.value = 'submit'

  try {
    // 1. Save all responses first
    const payload = buildResponsePayload()
    await api(`/api/v1/portal/forms/${submissionId}/responses`, {
      method: 'POST',
      body: payload
    })

    // 2. Finalize submission
    await api(`/api/v1/portal/forms/${submissionId}/submit`, {
      method: 'POST'
    })
    
    submission.value.status = 'completed'
    window.scrollTo({ top: 0, behavior: 'smooth' })
    alert('Form submitted successfully! Thank you.')
  } catch (err) {
    console.error('Failed to submit form', err)
    alert(err.data?.detail || 'Failed to submit form.')
  } finally {
    isSaving.value = false
    saveType.value = null
  }
}

onMounted(() => {
  fetchForm()
})
</script>
