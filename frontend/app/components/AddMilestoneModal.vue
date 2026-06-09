<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="close"></div>
    
    <!-- Modal Panel -->
    <div class="relative bg-[#171717] rounded-2xl shadow-xl w-full max-w-md border border-white/10 overflow-hidden animate-in zoom-in-95 duration-200">
      
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-white/5">
        <h3 class="text-lg font-bold text-white font-heading">Add Milestone</h3>
        <button @click="close" class="text-gray-400 hover:text-white transition-colors">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="submit" class="p-6 space-y-4">
        
        <!-- Error Message -->
        <div v-if="error" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg flex items-start gap-2">
          <AlertCircle class="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
          <p class="text-sm text-red-400">{{ error }}</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 font-mono">Milestone Title *</label>
          <input 
            v-model="form.title" 
            type="text" 
            required
            class="w-full bg-[#1e2020] border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#bef264] focus:border-transparent transition-all"
            placeholder="e.g. Design Handshake"
          />
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 font-mono">Description</label>
          <textarea 
            v-model="form.description" 
            rows="3"
            class="w-full bg-[#1e2020] border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#bef264] focus:border-transparent transition-all"
            placeholder="Optional details about this milestone..."
          ></textarea>
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 font-mono">Due Date</label>
          <input 
            v-model="form.due_date" 
            type="datetime-local" 
            class="w-full bg-[#1e2020] border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#bef264] focus:border-transparent transition-all [color-scheme:dark]"
          />
        </div>

        <!-- Footer Actions -->
        <div class="flex items-center justify-end gap-3 pt-4 border-t border-white/5 mt-6">
          <button 
            type="button" 
            @click="close"
            class="px-4 py-2 text-sm font-bold text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="px-5 py-2 text-sm font-bold bg-[#bef264] text-[#131f00] rounded-lg hover:bg-[#a4d64c] transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            <Loader2 v-if="isSubmitting" class="w-4 h-4 mr-2 animate-spin" />
            Save Milestone
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { X, AlertCircle, Loader2 } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

const props = defineProps({
  isOpen: Boolean,
  projectId: String
})

const emit = defineEmits(['close', 'milestone-added'])
const api = useApi()

const isSubmitting = ref(false)
const error = ref(null)

const form = reactive({
  title: '',
  description: '',
  due_date: ''
})

const close = () => {
  error.value = null
  form.title = ''
  form.description = ''
  form.due_date = ''
  emit('close')
}

const submit = async () => {
  if (!form.title) return
  
  error.value = null
  isSubmitting.value = true
  
  try {
    const payload = {
      title: form.title,
      description: form.description || null,
      due_date: form.due_date ? new Date(form.due_date).toISOString() : null,
      status: 'pending',
      sort_order: 0
    }
    
    const newMilestone = await api(`/api/v1/projects/${props.projectId}/milestones`, {
      method: 'POST',
      body: payload
    })
    
    emit('milestone-added', newMilestone)
    close()
  } catch (err) {
    error.value = err.message || 'Failed to create milestone'
  } finally {
    isSubmitting.value = false
  }
}
</script>
