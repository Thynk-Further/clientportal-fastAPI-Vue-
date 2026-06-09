<template>
  <div class="h-[calc(100vh-10rem)] min-h-[460px] max-w-7xl mx-auto font-sans text-[#e3e2e2] grid grid-cols-1 lg:grid-cols-12 border border-white/[0.08] rounded-xl overflow-hidden bg-[#171717]/60">
    
    <!-- LEFT PANEL: Threads -->
    <div class="lg:col-span-4 border-r border-white/5 flex flex-col bg-[#141414]">
      <div class="p-4 border-b border-white/5 bg-[#181818]/60 flex items-center justify-between">
        <span class="font-mono text-xs uppercase tracking-wider text-gray-400">Communication Channels</span>
        <button class="material-symbols-outlined text-gray-400 hover:text-[#bef264] text-lg cursor-pointer bg-transparent border-none">
          rate_review
        </button>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar divide-y divide-white/[0.03]">
        <div v-if="isLoading" class="p-4 space-y-4">
          <div v-for="i in 4" :key="i" class="animate-pulse flex gap-3">
            <div class="h-10 w-10 rounded-full bg-[#1e2020] shrink-0"></div>
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
          :class="`p-4 cursor-pointer transition-colors text-left flex items-start gap-3 group relative ${
            activeThreadId === th.id
              ? 'bg-gradient-to-r from-white/[0.03] to-transparent border-l-2 border-[#bef264] bg-[#1d1f1f]/80'
              : 'hover:bg-white/[0.01]'
          }`"
        >
          <!-- Custom Icon based on thread metadata -->
          <div :class="`h-10 w-10 rounded-full flex items-center justify-center shrink-0 ${
            activeThreadId === th.id
              ? 'bg-[#bef264]/10 text-[#bef264] border border-[#bef264]/20'
              : 'bg-[#1e2020] text-gray-400 border border-white/5'
          }`">
            <span class="material-symbols-outlined text-lg leading-none">
              chat
            </span>
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex justify-between items-baseline mb-0.5">
              <h4 :class="`font-bold text-sm truncate ${activeThreadId === th.id ? 'text-[#bef264]' : 'text-white group-hover:text-[#bef264] transition-colors'}`">
                {{ th.client ? th.client.name : 'Unknown Client' }}
              </h4>
              <span class="text-[10px] text-gray-500 font-mono shrink-0">{{ new Date(th.created_at).toLocaleDateString() }}</span>
            </div>
            <p class="text-[10px] text-gray-400 font-mono uppercase tracking-wider truncate mb-0.5">
              Project: {{ th.name }}
            </p>
            <p class="text-xs text-gray-500 truncate">{{ th.description || 'No recent messages' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT PANEL: Messages Board -->
    <div class="lg:col-span-8 flex flex-col bg-[#121414] relative">
      <div v-if="activeThread" class="flex-1 flex flex-col min-h-0">
        
        <!-- Recipient Header Node -->
        <header class="p-4 border-b border-white/5 bg-[#181818]/60 flex justify-between items-center z-10 shrink-0">
          <div class="flex items-center gap-3">
            <div class="h-9 w-9 bg-[#1e2020] rounded-full border border-white/5 flex items-center justify-center text-[#bef264]">
              <span class="material-symbols-outlined text-sm">
                chat
              </span>
            </div>
            <div class="min-w-0">
              <h3 class="font-display font-semibold text-white text-sm md:text-base leading-none truncate border-none">
                {{ activeThread.client ? activeThread.client.name : 'Unknown Client' }} <span class="text-gray-500 text-sm font-normal">— {{ activeThread.name }}</span>
              </h3>
              <p class="text-[10px] font-mono text-gray-400 uppercase tracking-wider mt-1.5 flex items-center gap-1 leading-none">
                <span class="h-1.5 w-1.5 rounded-full bg-green-400 animate-pulse"></span>
                Active Secure Connection
              </p>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <button class="material-symbols-outlined text-gray-400 hover:text-[#bef264] text-lg p-1.5 rounded-md cursor-pointer hover:bg-[#1e2020] bg-transparent border-none">
              phone
            </button>
            <button class="material-symbols-outlined text-gray-400 hover:text-[#bef264] text-lg p-1.5 rounded-md cursor-pointer hover:bg-[#1e2020] bg-transparent border-none">
              more_vert
            </button>
          </div>
        </header>

        <!-- Message logs flow -->
        <div class="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar bg-surface-container-lowest/10 relative" ref="messagesContainer">
          <div v-if="isLoadingMessages" class="flex justify-center p-4">
            <span class="material-symbols-outlined animate-spin text-[#bef264]">progress_activity</span>
          </div>
          
          <div v-else-if="activeMessages.length === 0" class="flex flex-col items-center justify-center h-full text-center opacity-50">
            <span class="material-symbols-outlined text-4xl mb-2">forum</span>
            <p class="text-sm">No messages in this project yet.</p>
          </div>

          <div
            v-else
            v-for="msg in activeMessages"
            :key="msg.id"
            :class="`flex gap-4 max-w-[85%] md:max-w-[70%] font-sans ${msg.sender_type === 'freelancer' ? 'ml-auto flex-row-reverse' : ''}`"
          >
            <!-- User avatar image -->
            <div class="h-9 w-9 bg-[#1e2020] text-gray-400 rounded-full flex items-center justify-center shrink-0 border border-white/5 select-none font-bold text-xs uppercase">
              {{ msg.sender_type === 'freelancer' ? 'YOU' : 'CLI' }}
            </div>

            <!-- Content body bubble -->
            <div class="space-y-1">
              <div :class="`flex items-baseline gap-2 mb-0.5 ${msg.sender_type === 'freelancer' ? 'flex-row-reverse font-sans' : ''}`">
                <span class="font-bold text-xs text-white">{{ msg.sender_type === 'freelancer' ? 'You' : 'Client' }}</span>
                <span class="text-[9px] font-mono text-gray-500">{{ new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}</span>
              </div>

              <div :class="`p-4 rounded-xl text-sm leading-relaxed border ${
                msg.sender_type === 'freelancer'
                  ? 'bg-[#1e2020] border-white/5 rounded-tr-none text-white'
                  : 'bg-[#bef264]/[0.03] border-[#bef264]/10 rounded-tl-none text-[#e2e2e2]'
              }`">
                <p>{{ msg.content }}</p>

                <!-- Attached File Document View -->
                <div v-if="msg.attachment" class="mt-3 p-3 bg-neutral-900/60 rounded-lg flex items-center justify-between border border-white/5 font-mono text-xs max-w-sm gap-2">
                  <div class="flex items-center gap-2 overflow-hidden">
                    <span class="material-symbols-outlined text-[#bef264] shrink-0 text-base">picture_as_pdf</span>
                    <span class="text-white truncate" :title="msg.attachment.name">{{ msg.attachment.name }}</span>
                    <span class="text-[10px] text-gray-400/80 shrink-0">({{ msg.attachment.size }})</span>
                  </div>
                  <button
                    class="material-symbols-outlined text-gray-400 hover:text-[#bef264] font-bold p-1 leading-none shrink-0"
                  >
                    download
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input section & attachments bar -->
        <div class="p-4 border-t border-white/5 bg-[#141414] shrink-0 space-y-3 z-10">
          
          <div 
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="onDropFile"
            :class="`p-3 bg-neutral-900 border rounded-lg flex flex-wrap items-center justify-between gap-3 text-xs transition-all ${
              isDragging ? 'border-[#bef264] bg-[#bef264]/[0.01]' : 'border-dashed border-white/5'
            }`"
          >
            <div class="flex items-center gap-2 text-gray-400 font-mono">
              <span class="material-symbols-outlined text-sm">cloud_upload</span>
              <span v-if="attachmentName" class="text-[#bef264] font-semibold truncate">{{ attachmentName }}</span>
              <span v-else>Drag & drop documents here / click clip icon</span>
            </div>
            
            <label class="cursor-pointer bg-white/5 border border-white/10 hover:border-[#bef264]/30 hover:bg-neutral-800 text-white font-mono text-[10px] uppercase font-bold py-1 px-2.5 rounded transition-all">
              Choose File
              <input type="file" @change="onFileSelect" class="sr-only" />
            </label>
          </div>

          <!-- Send bar panel -->
          <form @submit.prevent="handleSend" class="flex items-center gap-2">
            <input
              v-model="inputMessage"
              type="text"
              placeholder="Type secure client note or command response..."
              class="flex-1 bg-[#1e2020] text-sm text-white px-4 py-3 border border-white/5 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#bef264]"
              :disabled="isSending"
            />
            <button
              type="submit"
              :disabled="isSending"
              class="h-11 w-11 rounded-lg bg-[#bef264] text-[#131f00] hover:bg-[#bef264]/80 flex items-center justify-center shrink-0 cursor-pointer transition-all active:scale-95 border-none outline-none disabled:opacity-50"
              title="Send Message"
            >
              <span v-if="isSending" class="material-symbols-outlined text-md font-bold animate-spin">progress_activity</span>
              <span v-else class="material-symbols-outlined text-md font-bold">send</span>
            </button>
          </form>
        </div>

      </div>
      
      <div v-else class="flex-1 flex items-center justify-center text-gray-500 flex-col gap-3">
        <span class="material-symbols-outlined text-4xl opacity-50">forum</span>
        <p class="font-mono text-xs uppercase tracking-widest">Select a channel to connect</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useApi } from '~/composables/useApi'
import { useAuthStore } from '~/stores/auth'

const api = useApi()
const authStore = useAuthStore()

const threads = ref([])
const activeThreadId = ref(null)
const activeMessages = ref([])
const isLoading = ref(true)
const isLoadingMessages = ref(false)
const isSending = ref(false)

// Input states
const inputMessage = ref('')
const isDragging = ref(false)
const attachmentName = ref('')
const attachmentFile = ref(null)
const messagesContainer = ref(null)

const activeThread = computed(() => {
  return threads.value.find((t) => t.id === activeThreadId.value)
})

const clients = ref([])

const fetchThreads = async () => {
  try {
    // Fetch both projects and clients so we can map the client name to the project thread
    const [projectsData, clientsData] = await Promise.all([
      api('/api/v1/projects'),
      api('/api/v1/clients')
    ])
    
    // Create a dictionary for quick client lookups
    const clientMap = {}
    if (clientsData && clientsData.length) {
      clientsData.forEach(c => {
        clientMap[c.id] = c
      })
    }
    
    // Attach client details to each project thread
    threads.value = (projectsData || []).map(p => {
      return {
        ...p,
        client: clientMap[p.client_id] || null
      }
    })
    
    if (threads.value.length > 0 && !activeThreadId.value) {
      selectThread(threads.value[0].id)
    }
  } catch (err) {
    console.error('Failed to fetch projects and clients for threads', err)
  } finally {
    isLoading.value = false
  }
}

const selectThread = async (id) => {
  activeThreadId.value = id
  isLoadingMessages.value = true
  activeMessages.value = []
  
  // Close any existing connection
  if (ws.value) {
    ws.value.close()
    ws.value = null
  }
  
  try {
    const data = await api(`/api/v1/projects/${id}/messages`)
    activeMessages.value = data || []
    scrollToBottom()
    connectWebSocket(id)
  } catch (err) {
    console.error('Failed to fetch messages for project', err)
  } finally {
    isLoadingMessages.value = false
  }
}

let ws = ref(null)

const connectWebSocket = (projectId) => {
  const token = localStorage.getItem('access_token')
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  // Since we run FastAPI backend differently from frontend dev server, use the API baseURL
  const wsUrl = `ws://localhost:8000/api/v1/ws/projects/${projectId}?token=${token}`
  
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

const handleSend = async () => {
  if (!inputMessage.value.trim() && !attachmentFile.value) return
  if (!activeThreadId.value || !ws.value || ws.value.readyState !== WebSocket.OPEN) return

  isSending.value = true
  try {
    // Send message via WebSocket
    ws.value.send(inputMessage.value)
    
    inputMessage.value = ''
    attachmentName.value = ''
    attachmentFile.value = null
    scrollToBottom()
  } catch (err) {
    console.error('Failed to send message', err)
    alert('Failed to send message')
  } finally {
    isSending.value = false
  }
}

const onDropFile = (e) => {
  isDragging.value = false
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    attachmentFile.value = files[0]
    attachmentName.value = files[0].name
  }
}

const onFileSelect = (e) => {
  const target = e.target
  const files = target.files
  if (files && files.length > 0) {
    attachmentFile.value = files[0]
    attachmentName.value = files[0].name
  }
}

onMounted(() => {
  fetchThreads()
})
</script>
