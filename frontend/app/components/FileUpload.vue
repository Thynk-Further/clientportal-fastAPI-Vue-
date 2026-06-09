<template>
  <div class="mt-4 border border-dashed border-white/10 rounded-xl p-6 bg-layer-2 text-center relative group hover:bg-[#2e2e2e] transition-colors">
    <input 
      type="file" 
      @change="handleFileSelect" 
      :disabled="isUploading"
      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10 disabled:cursor-not-allowed" 
    />
    
    <div v-if="!isUploading" class="pointer-events-none">
      <div class="w-12 h-12 bg-layer-1 border border-white/5 rounded-xl shadow-sm flex items-center justify-center mx-auto mb-3">
        <UploadCloud class="w-6 h-6 text-accent" />
      </div>
      <p class="text-sm font-medium text-white font-heading">Click to upload or drag and drop</p>
      <p class="text-xs text-gray-400 mt-1 font-mono">SVG, PNG, JPG, PDF, ZIP up to 50MB</p>
    </div>

    <!-- Uploading State -->
    <div v-else class="py-2">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-white truncate pr-4">{{ selectedFile?.name }}</span>
        <span class="text-sm font-medium text-accent font-mono">{{ uploadProgress }}%</span>
      </div>
      <div class="w-full bg-layer-1 rounded-full h-2">
        <div class="bg-accent h-2 rounded-full transition-all duration-300" :style="{ width: `${uploadProgress}%` }"></div>
      </div>
      <p class="text-xs text-gray-400 mt-3 text-left font-mono">Uploading to secure storage...</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="absolute top-full left-0 right-0 mt-2 p-2 bg-red-900/20 text-red-400 text-xs rounded border border-red-900/50 z-20">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UploadCloud } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

const props = defineProps({
  deliverableId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['upload-complete'])
const api = useApi()

const isUploading = ref(false)
const uploadProgress = ref(0)
const selectedFile = ref(null)
const error = ref(null)

const handleFileSelect = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Basic validation
  if (file.size > 50 * 1024 * 1024) {
    error.value = 'File is too large. Max size is 50MB.'
    return
  }

  selectedFile.value = file
  error.value = null
  isUploading.value = true
  uploadProgress.value = 10

  try {
    // 1. Get presigned URL
    const presignData = await api('/api/v1/files/presigned-url', {
      method: 'POST',
      body: {
        deliverable_id: props.deliverableId,
        filename: file.name,
        content_type: file.type || 'application/octet-stream'
      }
    })

    uploadProgress.value = 30

    // 2. Upload directly to R2 using native fetch/XHR (XHR gives upload progress!)
    await new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          // Map progress from 30% to 90%
          const percentComplete = Math.round((e.loaded / e.total) * 100)
          uploadProgress.value = 30 + Math.floor(percentComplete * 0.6)
        }
      })

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve()
        } else {
          reject(new Error(`Upload failed with status ${xhr.status}`))
        }
      }

      xhr.onerror = () => reject(new Error('Network error during upload'))

      xhr.open('PUT', presignData.presigned_url, true)
      xhr.setRequestHeader('Content-Type', file.type || 'application/octet-stream')
      xhr.send(file)
    })

    uploadProgress.value = 95

    // 3. Confirm upload with backend
    const confirmedFile = await api('/api/v1/files/confirm', {
      method: 'POST',
      body: {
        deliverable_id: props.deliverableId,
        object_key: presignData.object_key,
        file_size: file.size,
        mime_type: file.type || 'application/octet-stream',
        file_name: file.name
      }
    })

    uploadProgress.value = 100
    
    // Reset and emit
    setTimeout(() => {
      isUploading.value = false
      selectedFile.value = null
      uploadProgress.value = 0
      emit('upload-complete', confirmedFile)
    }, 500)

  } catch (err) {
    console.error('Upload flow failed:', err)
    error.value = err.data?.detail || err.message || 'Upload failed. Please try again.'
    isUploading.value = false
    uploadProgress.value = 0
  }
  
  // Reset the input
  event.target.value = ''
}
</script>
