<template>
  <div class="space-y-8 font-sans max-w-4xl mx-auto text-[#e3e2e2]">
    
    <!-- Navigation Back -->
    <div>
      <NuxtLink to="/forms" class="text-xs font-mono uppercase tracking-widest text-gray-500 hover:text-[#bef264] transition-colors flex items-center gap-1 w-fit">
        <span class="material-symbols-outlined text-sm">arrow_back</span>
        Back to Forms
      </NuxtLink>
    </div>

    <div v-if="isLoading" class="flex justify-center p-20">
      <span class="material-symbols-outlined animate-spin text-4xl text-[#bef264]">progress_activity</span>
    </div>

    <div v-else-if="submission" class="space-y-8">
      
      <!-- Submission Header -->
      <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden p-8">
        <div class="flex flex-col md:flex-row justify-between gap-6 mb-6">
          <div>
            <h1 class="font-display text-3xl font-bold text-white mb-2">{{ submission.title }}</h1>
            <div class="flex flex-wrap items-center gap-4 text-sm text-gray-400 font-mono">
              <span class="flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">folder</span>
                Project: <span class="text-white">{{ submission.project?.name || submission.project_id }}</span>
              </span>
              <span class="flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">calendar_today</span>
                Assigned: <span class="text-white">{{ new Date(submission.created_at).toLocaleDateString() }}</span>
              </span>
            </div>
          </div>
          <div>
            <span :class="`px-3 py-1.5 rounded-lg text-xs font-bold border uppercase tracking-wider ${
              submission.status === 'completed' ? 'bg-green-500/10 text-green-400 border-green-500/20' :
              submission.status === 'partial' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
              'bg-white/5 text-gray-400 border-white/10'
            }`">
              {{ submission.status }}
            </span>
          </div>
        </div>

        <div v-if="submission.status === 'completed'" class="bg-[#bef264]/10 border border-[#bef264]/20 rounded-lg p-4 flex items-start gap-3">
          <span class="material-symbols-outlined text-[#bef264] mt-0.5">check_circle</span>
          <div>
            <h3 class="font-bold text-[#bef264] text-sm">Submission Complete</h3>
            <p class="text-xs text-gray-400 mt-1">The client completed this form on {{ new Date(submission.submitted_at).toLocaleString() }}</p>
          </div>
        </div>
      </div>

      <!-- Responses List -->
      <div class="space-y-4">
        <h3 class="font-display text-xl font-bold text-white mb-4">Client Responses</h3>
        
        <div v-if="submission.responses && submission.responses.length > 0" class="space-y-4">
          <div v-for="response in submission.responses" :key="response.id" class="bg-[#171717] border border-white/[0.08] rounded-xl p-6">
            <!-- Note: In a full app we'd map field_id to field label by fetching the template too. For now we show response basics. -->
            <div class="text-xs font-mono text-gray-500 mb-2 uppercase tracking-widest">Field ID: {{ response.form_field_id }}</div>
            
            <div v-if="response.value_text" class="text-white bg-[#1e2020] p-4 rounded-lg border border-white/5 mt-3 whitespace-pre-wrap">
              {{ response.value_text }}
            </div>
            
            <div v-else-if="response.value_file_url || response.value_file_object_key" class="mt-3 flex items-center gap-3 bg-[#1e2020] border border-white/5 p-4 rounded-lg w-fit">
               <span class="material-symbols-outlined text-[#bef264]">attachment</span>
               <span class="text-sm text-white font-mono">{{ response.value_file_object_key || 'File Uploaded' }}</span>
            </div>
            
            <div v-else class="text-sm text-gray-500 italic mt-3">
              No response provided.
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-12 bg-[#171717] border border-white/[0.08] rounded-xl opacity-80">
          <span class="material-symbols-outlined text-4xl text-gray-400/40 mb-3">
            chat_bubble_outline
          </span>
          <p class="text-sm text-gray-400">No responses recorded yet.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from '#app'
import { useApi } from '~/composables/useApi'

const route = useRoute()
const api = useApi()

const isLoading = ref(true)
const submission = ref(null)

const fetchSubmission = async () => {
  try {
    submission.value = await api(`/api/v1/form-submissions/${route.params.id}`)
  } catch (error) {
    console.error('Failed to fetch submission details', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchSubmission()
})
</script>
