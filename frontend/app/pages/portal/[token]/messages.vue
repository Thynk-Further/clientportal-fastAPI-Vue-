<template>
  <div class="h-[calc(100vh-180px)] md:h-[calc(100vh-140px)] flex flex-col md:flex-row gap-6 font-sans text-[#e3e2e2] max-w-7xl mx-auto w-full">
    
    <!-- Left Column: Recent Chats -->
    <div class="w-full md:w-80 flex-shrink-0 flex flex-col bg-[#171717] rounded-xl border border-white/5 overflow-hidden">
      <div class="p-4 border-b border-white/5 flex justify-between items-center">
        <h2 class="font-display font-bold text-white text-lg">Recent Chats</h2>
      </div>
      
      <div class="flex-1 overflow-y-auto custom-scrollbar divide-y divide-white/[0.03]">
        <div v-if="isLoading" class="p-4 space-y-4">
          <div v-for="i in 4" :key="i" class="animate-pulse flex gap-3">
            <div class="h-10 w-10 rounded-lg bg-[#1e2020] shrink-0"></div>
            <div class="flex-1 space-y-2">
              <div class="h-3 bg-[#1e2020] rounded w-1/2"></div>
              <div class="h-2 bg-[#1e2020] rounded w-3/4"></div>
            </div>
          </div>
        </div>

        <div
          v-else
          v-for="th in threads"
          :key="th.id"
          @click="selectThread(th.id)"
          :class="`p-4 border-l-2 cursor-pointer transition-colors relative ${
            activeThreadId === th.id
              ? 'bg-white/[0.02] border-l-[#bef264] hover:bg-white/[0.04]'
              : 'border-l-transparent hover:bg-white/[0.02] opacity-70 hover:opacity-100'
          }`"
        >
          <div class="flex items-center gap-3">
            <div :class="`w-10 h-10 rounded-lg border flex items-center justify-center ${
              activeThreadId === th.id ? 'bg-[#1e2020] border-white/10 text-[#bef264]' : 'bg-[#1e2020] border-white/10 text-gray-400'
            }`">
              <span class="material-symbols-outlined text-xl">architecture</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-baseline mb-0.5">
                <h4 class="font-bold text-white text-sm truncate">{{ th.name }}</h4>
              </div>
              <p :class="`text-xs truncate ${activeThreadId === th.id ? 'text-[#bef264]' : 'text-gray-400'}`">Project discussion...</p>
            </div>
          </div>
        </div>

        <div v-if="!isLoading && threads.length === 0" class="p-6 text-center text-gray-500 text-sm">
          No active projects found.
        </div>
      </div>
    </div>

    <!-- Right Column: Chat Interface -->
    <div class="flex-1 flex flex-col bg-[#121414] rounded-xl border border-white/5 overflow-hidden relative">
      <template v-if="activeThread">
        <!-- Chat Header -->
        <div class="h-16 border-b border-white/5 flex items-center justify-between px-6 bg-[#171717] shrink-0">
          <div>
            <h2 class="font-display font-bold text-white text-lg flex items-center gap-2">
              {{ activeThread.name }}
            </h2>
            <div class="flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-widest text-[#bef264] mt-0.5">
              <span class="w-1.5 h-1.5 bg-[#bef264] rounded-full"></span>
              Secure Connection
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button class="w-9 h-9 rounded bg-[#1e2020] border border-white/5 hover:bg-white/10 text-gray-300 flex items-center justify-center transition-colors">
              <span class="material-symbols-outlined text-[18px]">call</span>
            </button>
            <button class="w-9 h-9 rounded bg-[#1e2020] border border-white/5 hover:bg-white/10 text-gray-300 flex items-center justify-center transition-colors">
              <span class="material-symbols-outlined text-[18px]">videocam</span>
            </button>
            <button class="w-9 h-9 rounded bg-transparent hover:bg-white/5 text-gray-400 flex items-center justify-center transition-colors">
              <span class="material-symbols-outlined text-[18px]">more_vert</span>
            </button>
          </div>
        </div>

        <!-- Chat Messages Area -->
        <div class="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar bg-[radial-gradient(ellipse_at_top_right,rgba(190,242,100,0.02),transparent_50%)]" ref="messagesContainer">
          
          <div v-if="isLoadingMessages" class="flex justify-center p-4">
            <span class="material-symbols-outlined animate-spin text-[#bef264]">progress_activity</span>
          </div>

          <div v-else-if="activeMessages.length === 0" class="flex flex-col items-center justify-center h-full text-center opacity-50 text-gray-400">
            <span class="material-symbols-outlined text-4xl mb-2">forum</span>
            <p class="text-sm">No messages yet. Say hello!</p>
          </div>

          <div
            v-else
            v-for="msg in activeMessages"
            :key="msg.id"
            :class="`flex gap-4 ${msg.sender_type === 'client' ? 'flex-row-reverse' : ''}`"
          >
            <!-- User avatar image -->
            <div :class="`w-8 h-8 rounded-full flex items-center justify-center font-bold shrink-0 mt-6 border ${
              msg.sender_type === 'client'
                ? 'overflow-hidden border-white/10 bg-gray-600 text-white text-xs'
                : 'bg-[#bef264] text-[#131f00] border-[#bef264]/20 shadow-[0_0_10px_rgba(190,242,100,0.2)]'
            }`">
              <span v-if="msg.sender_type !== 'client'" class="material-symbols-outlined text-[16px]">bolt</span>
              <span v-else>YOU</span>
            </div>
            
            <div :class="`flex flex-col gap-1 max-w-[80%] ${msg.sender_type === 'client' ? 'items-end' : ''}`">
              <span :class="`text-[10px] font-mono text-gray-500 ${msg.sender_type === 'client' ? 'mr-1' : 'ml-1'}`">
                {{ msg.sender_type === 'client' ? 'You' : 'PortalX Team' }}
              </span>
              
              <div :class="`p-4 text-sm leading-relaxed shadow-sm ${
                msg.sender_type === 'client'
                  ? 'bg-[#bef264] text-[#131f00] rounded-2xl rounded-tr-sm font-medium'
                  : 'bg-[#1e2020] text-white rounded-2xl rounded-tl-sm border border-white/5'
              }`">
                <p>{{ msg.content }}</p>

                <!-- Attached File Document View -->
                <div v-if="msg.attachment" class="mt-3 p-3 bg-neutral-900/60 rounded-lg flex items-center justify-between border border-white/5 font-mono text-xs max-w-sm gap-2">
                  <div class="flex items-center gap-2 overflow-hidden">
                    <span class="material-symbols-outlined text-[#bef264] shrink-0 text-base">picture_as_pdf</span>
                    <span class="text-white truncate" :title="msg.attachment.name">{{ msg.attachment.name }}</span>
                    <span class="text-[10px] text-gray-400/80 shrink-0">({{ msg.attachment.size }})</span>
                  </div>
                  <button class="material-symbols-outlined text-gray-400 hover:text-[#bef264] font-bold p-1 leading-none shrink-0">
                    download
                  </button>
                </div>
              </div>
              <span :class="`text-[9px] text-gray-500 ${msg.sender_type === 'client' ? 'mr-2' : 'ml-2'}`">
                {{ new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Chat Input Area -->
        <div class="p-4 bg-[#171717] border-t border-white/5 shrink-0">
          <form @submit.prevent="handleSend" class="bg-[#1e2020] border border-white/10 rounded-xl p-2 flex items-end gap-2 focus-within:border-[#bef264]/50 transition-colors shadow-sm">
            <div class="flex gap-1 pb-1 px-1">
              <button type="button" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white rounded-full hover:bg-white/5 transition-colors">
                <span class="material-symbols-outlined text-[20px]">add_circle</span>
              </button>
              <button type="button" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white rounded-full hover:bg-white/5 transition-colors">
                <span class="material-symbols-outlined text-[20px]">attach_file</span>
              </button>
            </div>
            
            <textarea 
              v-model="inputMessage"
              @keydown.enter.prevent="handleEnter"
              rows="1" 
              placeholder="Type your message to the team..." 
              class="flex-1 bg-transparent border-none text-sm text-white resize-none outline-none py-2.5 max-h-32 custom-scrollbar placeholder-gray-500"
              :disabled="isSending"
            ></textarea>
            
            <button 
              type="submit"
              :disabled="isSending || !inputMessage.trim()"
              class="w-10 h-10 rounded-lg bg-[#bef264] text-[#131f00] flex items-center justify-center hover:bg-[#a3d64c] transition-colors shadow-sm shrink-0 mb-0.5 mr-0.5 disabled:opacity-50"
            >
              <span v-if="isSending" class="material-symbols-outlined text-[18px] animate-spin">progress_activity</span>
              <span v-else class="material-symbols-outlined text-[18px]">send</span>
            </button>
          </form>
          <div class="flex justify-between items-center mt-2 px-2">
            <span class="text-[9px] font-mono text-gray-600 uppercase tracking-widest">Enter to send, Shift + Enter for new line</span>
            <span class="text-[9px] font-mono text-gray-600 flex items-center gap-1"><span class="material-symbols-outlined text-[12px]">schedule</span> Replies within 2 hours</span>
          </div>
        </div>
      </template>

      <div v-else class="flex-1 flex items-center justify-center text-gray-500 flex-col gap-3">
        <span class="material-symbols-outlined text-4xl opacity-50">forum</span>
        <p class="font-mono text-xs uppercase tracking-widest">Select a project chat</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '~/composables/useApi'
import { useRuntimeConfig } from '#app'

definePageMeta({
  layout: 'portal'
})

const route = useRoute()
const api = useApi()
const config = useRuntimeConfig()

const threads = ref([])
const activeThreadId = ref(null)
const activeMessages = ref([])
const isLoading = ref(true)
const isLoadingMessages = ref(false)
const isSending = ref(false)
const inputMessage = ref('')
const messagesContainer = ref(null)

let ws = ref(null)

const activeThread = computed(() => {
  return threads.value.find((t) => t.id === activeThreadId.value)
})

const fetchThreads = async () => {
  try {
    const projectsData = await api('/api/v1/portal/projects')
    threads.value = projectsData || []
    
    if (threads.value.length > 0 && !activeThreadId.value) {
      selectThread(threads.value[0].id)
    }
  } catch (err) {
    console.error('Failed to fetch projects for threads', err)
  } finally {
    isLoading.value = false
  }
}

const selectThread = async (id) => {
  activeThreadId.value = id
  isLoadingMessages.value = true
  activeMessages.value = []
  
  if (ws.value) {
    ws.value.close()
    ws.value = null
  }
  
  try {
    const data = await api(`/api/v1/portal/projects/${id}/messages`)
    activeMessages.value = data || []
    scrollToBottom()
    connectWebSocket(id)
  } catch (err) {
    console.error('Failed to fetch messages', err)
  } finally {
    isLoadingMessages.value = false
  }
}

const connectWebSocket = (projectId) => {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  // Extract domain from apiBaseUrl
  const baseUrl = config.public.apiBaseUrl.replace(/^https?:\/\//, '')
  const wsUrl = `${wsProtocol}//${baseUrl}/api/v1/ws/projects/${projectId}`
  
  ws.value = new WebSocket(wsUrl)
  
  ws.value.onopen = () => {
    console.log('WebSocket connection established.')
  }
  
  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    activeMessages.value.push(data)
    scrollToBottom()
  }
  
  ws.value.onerror = (error) => {
    console.error('WebSocket Error: ', error)
  }
  
  ws.value.onclose = () => {
    console.log('WebSocket connection closed.')
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleEnter = (e) => {
  if (e.shiftKey) return
  handleSend()
}

const handleSend = async () => {
  if (!inputMessage.value.trim()) return
  if (!activeThreadId.value || !ws.value || ws.value.readyState !== WebSocket.OPEN) {
    alert("Chat is not connected.")
    return
  }

  isSending.value = true
  try {
    ws.value.send(inputMessage.value)
    inputMessage.value = ''
    scrollToBottom()
  } catch (err) {
    console.error('Failed to send message', err)
    alert('Failed to send message')
  } finally {
    isSending.value = false
  }
}

onMounted(() => {
  fetchThreads()
})
</script>
