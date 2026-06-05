<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    <!-- Header -->
    <section class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
          Time & Work Ledger
        </h2>
        <p class="text-xs text-gray-400 mt-2">
          Track billable hours, manage active sprints, and log manual entries for future invoicing.
        </p>
      </div>
      <div class="flex gap-2">
        <button
          @click="showManualModal = true"
          class="bg-[#1e2020] text-gray-300 hover:bg-[#2a2c2c] hover:text-white border border-white/5 font-bold px-5 py-3 rounded-lg text-sm transition-all duration-100 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider"
        >
          <span class="material-symbols-outlined text-md">history_edu</span>
          Log Manually
        </button>
      </div>
    </section>

    <!-- Project Selector for Time Context -->
    <section class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col md:flex-row gap-4 items-center justify-between">
      <div class="flex-1 w-full flex items-center gap-4">
        <div class="bg-[#bef264]/10 text-[#bef264] p-3 rounded-xl shrink-0 hidden md:block">
          <span class="material-symbols-outlined text-xl leading-none">timer</span>
        </div>
        <div class="w-full md:w-auto">
          <label class="font-mono text-[10px] uppercase tracking-wider text-gray-500 mb-1 block">Context Sprint (Project)</label>
          <select
            v-model="activeProjectId"
            @change="handleProjectChange"
            class="bg-[#1e2020] text-white border border-white/5 rounded-lg p-2.5 text-sm outline-none focus:ring-1 focus:ring-[#bef264] min-w-[250px] w-full"
            :disabled="activeTimer !== null"
          >
            <option value="" disabled>Select a project to track...</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">
              {{ p.name }}
            </option>
          </select>
        </div>
      </div>
    </section>

    <div v-if="activeProjectId" class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- LEFT: Live Timer Widget -->
      <div class="lg:col-span-4 space-y-6">
        <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden relative group">
          <!-- Active Gradient Border Effect -->
          <div v-if="activeTimer" class="absolute inset-0 bg-gradient-to-r from-[#bef264]/20 to-transparent pointer-events-none opacity-50 animate-pulse"></div>

          <div class="p-6 relative z-10 flex flex-col items-center justify-center min-h-[300px]">
            <span class="font-mono text-xs text-gray-400 uppercase tracking-widest mb-4">Live Session</span>
            
            <div class="font-mono text-5xl font-extrabold text-white tracking-tighter tabular-nums mb-8 drop-shadow-lg">
              {{ formatDuration(currentTimerSeconds) }}
            </div>

            <div class="w-full space-y-4">
              <input
                v-model="timerDescription"
                type="text"
                placeholder="What are you working on?"
                class="w-full bg-[#1e2020]/50 border border-white/5 rounded-lg p-3 text-sm text-center text-white focus:outline-none focus:border-[#bef264]/50 transition-colors placeholder:text-gray-600"
                :disabled="activeTimer !== null"
              />
              
              <button
                v-if="!activeTimer"
                @click="startTimer"
                :disabled="isTimerSubmitting"
                class="w-full bg-[#bef264] text-[#131f00] hover:bg-[#bef264]/80 font-bold py-3.5 rounded-lg text-sm transition-all duration-200 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider disabled:opacity-50"
              >
                <span v-if="isTimerSubmitting" class="material-symbols-outlined animate-spin text-lg">progress_activity</span>
                <span v-else class="material-symbols-outlined text-lg">play_arrow</span>
                Start Tracking
              </button>

              <button
                v-else
                @click="stopTimer"
                :disabled="isTimerSubmitting"
                class="w-full bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 font-bold py-3.5 rounded-lg text-sm transition-all duration-200 cursor-pointer active:scale-95 flex items-center justify-center gap-2 font-mono uppercase tracking-wider disabled:opacity-50"
              >
                <span v-if="isTimerSubmitting" class="material-symbols-outlined animate-spin text-lg">progress_activity</span>
                <span v-else class="material-symbols-outlined text-lg">stop</span>
                Stop Session
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Historical Ledger -->
      <div class="lg:col-span-8">
        <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden flex flex-col h-full min-h-[400px]">
          <div class="p-5 border-b border-white/5 bg-[#181818]/60 flex items-center justify-between">
            <h3 class="font-bold text-white font-mono text-sm uppercase tracking-wider">Session Ledger</h3>
            <span class="text-xs text-[#bef264] bg-[#bef264]/10 px-2.5 py-1 rounded-md font-mono">{{ totalProjectHours.toFixed(1) }}h Total</span>
          </div>

          <div v-if="isLoadingEntries" class="flex-1 flex items-center justify-center">
            <span class="material-symbols-outlined animate-spin text-3xl text-[#bef264]/50">progress_activity</span>
          </div>

          <div v-else-if="timeEntries.length === 0" class="flex-1 flex flex-col items-center justify-center text-center p-8 opacity-50">
            <span class="material-symbols-outlined text-5xl mb-3">history_toggle_off</span>
            <p class="font-mono text-xs uppercase tracking-widest text-gray-400">No time tracked for this sprint</p>
          </div>

          <div v-else class="flex-1 overflow-x-auto custom-scrollbar">
            <table class="w-full text-left text-sm whitespace-nowrap">
              <thead class="bg-white/[0.02] border-b border-white/[0.05] font-mono text-[10px] uppercase tracking-wider text-gray-500">
                <tr>
                  <th class="px-5 py-3">Task / Description</th>
                  <th class="px-5 py-3">Date</th>
                  <th class="px-5 py-3 text-right">Duration</th>
                  <th class="px-5 py-3 text-right">Revenue</th>
                  <th class="px-5 py-3 text-center">Status</th>
                  <th class="px-5 py-3"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/[0.05] font-sans">
                <tr v-for="entry in timeEntries" :key="entry.id" class="hover:bg-white/[0.01] transition-colors group">
                  <td class="px-5 py-4">
                    <div class="font-medium text-white truncate max-w-[200px]" :title="entry.description || 'Untitled Session'">
                      {{ entry.description || 'Untitled Session' }}
                    </div>
                    <div class="text-[10px] text-gray-500 font-mono mt-0.5">
                      {{ formatTimeRange(entry.started_at, entry.ended_at) }}
                    </div>
                  </td>
                  <td class="px-5 py-4 text-gray-400 font-mono text-xs">
                    {{ new Date(entry.started_at).toLocaleDateString() }}
                  </td>
                  <td class="px-5 py-4 text-right font-mono font-bold text-white">
                    <span v-if="entry.ended_at">{{ formatDuration(entry.duration_seconds) }}</span>
                    <span v-else class="text-[#bef264] animate-pulse">Running...</span>
                  </td>
                  <td class="px-5 py-4 text-right font-mono text-xs">
                    <span v-if="!entry.is_billable" class="text-gray-500">Non-billable</span>
                    <span v-else-if="entry.duration_seconds" class="text-green-400 font-bold">${{ calculateRevenue(entry.duration_seconds, entry.hourly_rate_cents) }}</span>
                    <span v-else class="text-gray-500">-</span>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <span v-if="entry.invoice_id" class="px-2 py-1 rounded text-[9px] font-bold border uppercase tracking-wider bg-blue-500/10 text-blue-400 border-blue-500/20">Invoiced</span>
                    <span v-else-if="entry.is_billable && entry.ended_at" class="px-2 py-1 rounded text-[9px] font-bold border uppercase tracking-wider bg-green-500/10 text-green-400 border-green-500/20">Unbilled</span>
                    <span v-else-if="!entry.ended_at" class="px-2 py-1 rounded text-[9px] font-bold border uppercase tracking-wider bg-[#bef264]/10 text-[#bef264] border-[#bef264]/20">Active</span>
                  </td>
                  <td class="px-5 py-4 text-right">
                    <button
                      v-if="!entry.invoice_id && entry.ended_at"
                      @click="deleteEntry(entry.id)"
                      class="p-1.5 opacity-0 group-hover:opacity-100 hover:bg-red-500/10 hover:text-red-400 text-gray-500 rounded transition-all cursor-pointer"
                      title="Delete Entry"
                    >
                      <span class="material-symbols-outlined text-base leading-none">delete</span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State when no project is selected -->
    <div v-if="!activeProjectId" class="text-center py-20 bg-[#171717] border border-white/[0.08] rounded-xl opacity-80">
      <span class="material-symbols-outlined text-5xl text-gray-400/40 mb-3 animate-pulse">
        account_tree
      </span>
      <h3 class="text-lg font-bold text-white mb-1">No Context Selected</h3>
      <p class="text-gray-400 font-mono text-xs max-w-md mx-auto">Select a project from the dropdown above to view its time ledger or start tracking a new session.</p>
    </div>

    <!-- MANUAL LOGGING MODAL -->
    <div v-if="showManualModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-8 max-w-md w-full space-y-6">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-xl font-bold text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-[#bef264]">history_edu</span>
            Log Historical Session
          </h4>
          <button
            @click="showManualModal = false"
            class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer transition-colors"
          >
            close
          </button>
        </div>

        <form @submit.prevent="submitManualEntry" class="space-y-4 font-sans text-sm">
          <div v-if="manualError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
            {{ manualError }}
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Project Context</label>
            <select
              v-model="manualForm.project_id"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none appearance-none"
              :disabled="isManualSubmitting"
            >
              <option value="" disabled>Select a project...</option>
              <option v-for="p in projects" :key="p.id" :value="p.id">
                {{ p.name }}
              </option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Description</label>
            <input
              v-model="manualForm.description"
              type="text"
              placeholder="e.g. Research and wireframing"
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="isManualSubmitting"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Start Time</label>
              <input
                v-model="manualForm.started_at"
                type="datetime-local"
                required
                class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none [color-scheme:dark]"
                :disabled="isManualSubmitting"
              />
            </div>
            <div class="space-y-1">
              <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">End Time</label>
              <input
                v-model="manualForm.ended_at"
                type="datetime-local"
                required
                class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none [color-scheme:dark]"
                :disabled="isManualSubmitting"
              />
            </div>
          </div>

          <div class="flex items-center gap-2 pt-2">
            <input
              v-model="manualForm.is_billable"
              type="checkbox"
              id="is_billable"
              class="accent-[#bef264] w-4 h-4 cursor-pointer"
            />
            <label for="is_billable" class="text-white text-sm cursor-pointer select-none">This session is billable</label>
          </div>

          <div class="flex justify-end gap-2 text-sm pt-4">
            <button
              type="button"
              @click="showManualModal = false"
              :disabled="isManualSubmitting"
              class="px-5 py-2.5 rounded-lg hover:bg-white/[0.05] transition-colors disabled:opacity-50 text-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isManualSubmitting"
              class="px-6 py-2.5 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg cursor-pointer transform active:scale-95 transition-all text-xs uppercase font-mono tracking-wider disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="isManualSubmitting" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
              Save Ledger Entry
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useApi } from '~/composables/useApi'

const api = useApi()

// Global States
const projects = ref([])
const activeProjectId = ref('')
const timeEntries = ref([])
const isLoadingEntries = ref(false)

// Timer States
const activeTimer = ref(null) // The currently running entry object from backend
const timerDescription = ref('')
const isTimerSubmitting = ref(false)
const currentTimerSeconds = ref(0)
let timerInterval = null

// Manual Logging States
const showManualModal = ref(false)
const isManualSubmitting = ref(false)
const manualError = ref('')
const manualForm = ref({
  project_id: '',
  description: '',
  started_at: '',
  ended_at: '',
  is_billable: true
})

const totalProjectHours = computed(() => {
  const totalSecs = timeEntries.value.reduce((acc, entry) => {
    return acc + (entry.duration_seconds || 0)
  }, 0)
  // add live timer
  const liveSecs = activeTimer.value ? currentTimerSeconds.value : 0
  return (totalSecs + liveSecs) / 3600
})

const fetchProjects = async () => {
  try {
    projects.value = await api('/api/v1/projects')
  } catch (err) {
    console.error('Failed to fetch projects', err)
  }
}

const handleProjectChange = async () => {
  if (!activeProjectId.value) return
  isLoadingEntries.value = true
  try {
    timeEntries.value = await api(`/api/v1/projects/${activeProjectId.value}/time-entries`)
    
    // Check if one of them is actively running
    const active = timeEntries.value.find(e => !e.ended_at)
    if (active) {
      activeTimer.value = active
      timerDescription.value = active.description || ''
      startTicking()
    } else {
      activeTimer.value = null
      timerDescription.value = ''
      stopTicking()
    }
  } catch (err) {
    console.error('Failed to fetch time entries', err)
  } finally {
    isLoadingEntries.value = false
  }
}

const startTicking = () => {
  stopTicking()
  if (!activeTimer.value) return
  
  const startMs = new Date(activeTimer.value.started_at + 'Z').getTime() // parse as UTC
  
  const tick = () => {
    const nowMs = new Date().getTime()
    currentTimerSeconds.value = Math.floor((nowMs - startMs) / 1000)
    // Failsafe negative
    if (currentTimerSeconds.value < 0) currentTimerSeconds.value = 0
  }
  
  tick() // initial
  timerInterval = setInterval(tick, 1000)
}

const stopTicking = () => {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
  currentTimerSeconds.value = 0
}

const startTimer = async () => {
  if (!activeProjectId.value) return
  isTimerSubmitting.value = true
  try {
    const newEntry = await api(`/api/v1/projects/${activeProjectId.value}/time-entries/start`, {
      method: 'POST',
      body: {
        description: timerDescription.value || null,
        is_billable: true
      }
    })
    
    // Add to top of list
    timeEntries.value.unshift(newEntry)
    activeTimer.value = newEntry
    startTicking()
  } catch (err) {
    alert(err.data?.detail || 'Failed to start timer. Check if another timer is running.')
  } finally {
    isTimerSubmitting.value = false
  }
}

const stopTimer = async () => {
  if (!activeTimer.value) return
  isTimerSubmitting.value = true
  try {
    const updatedEntry = await api(`/api/v1/time-entries/${activeTimer.value.id}/stop`, {
      method: 'POST'
    })
    
    // Update in list
    const idx = timeEntries.value.findIndex(e => e.id === updatedEntry.id)
    if (idx !== -1) {
      timeEntries.value[idx] = updatedEntry
    }
    
    activeTimer.value = null
    timerDescription.value = ''
    stopTicking()
  } catch (err) {
    alert(err.data?.detail || 'Failed to stop timer.')
  } finally {
    isTimerSubmitting.value = false
  }
}

const submitManualEntry = async () => {
  manualError.value = ''
  isManualSubmitting.value = true
  
  try {
    // Format local datetime-local to UTC ISO string
    const startIso = new Date(manualForm.value.started_at).toISOString()
    const endIso = new Date(manualForm.value.ended_at).toISOString()
    
    if (new Date(endIso) <= new Date(startIso)) {
      throw new Error("End time must be after start time")
    }

    const entry = await api(`/api/v1/projects/${manualForm.value.project_id}/time-entries/manual`, {
      method: 'POST',
      body: {
        description: manualForm.value.description || null,
        started_at: startIso,
        ended_at: endIso,
        is_billable: manualForm.value.is_billable
      }
    })
    
    // If the active project is the one we just logged to, add it to the list
    if (activeProjectId.value === manualForm.value.project_id) {
      timeEntries.value.unshift(entry)
      // Sort by started_at desc
      timeEntries.value.sort((a, b) => new Date(b.started_at) - new Date(a.started_at))
    }
    
    showManualModal.value = false
    manualForm.value = {
      project_id: '',
      description: '',
      started_at: '',
      ended_at: '',
      is_billable: true
    }
  } catch (err) {
    manualError.value = err.message || err.data?.detail || 'Failed to save manual entry.'
  } finally {
    isManualSubmitting.value = false
  }
}

const deleteEntry = async (id) => {
  if (!confirm("Are you sure you want to delete this time entry? This cannot be undone.")) return
  
  try {
    await api(`/api/v1/time-entries/${id}`, { method: 'DELETE' })
    timeEntries.value = timeEntries.value.filter(e => e.id !== id)
  } catch(err) {
    alert(err.data?.detail || "Failed to delete.")
  }
}

// Helpers
const formatDuration = (totalSeconds) => {
  if (!totalSeconds || totalSeconds < 0) return '00:00:00'
  const h = Math.floor(totalSeconds / 3600).toString().padStart(2, '0')
  const m = Math.floor((totalSeconds % 3600) / 60).toString().padStart(2, '0')
  const s = (totalSeconds % 60).toString().padStart(2, '0')
  return `${h}:${m}:${s}`
}

const formatTimeRange = (start, end) => {
  if (!start) return ''
  const s = new Date(start + 'Z').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  if (!end) return `${s} - Present`
  const e = new Date(end + 'Z').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  return `${s} - ${e}`
}

const calculateRevenue = (durationSecs, rateCents) => {
  if (!durationSecs || !rateCents) return '0.00'
  const hours = durationSecs / 3600
  const dollars = (hours * rateCents) / 100
  return dollars.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

onMounted(() => {
  fetchProjects()
})

onUnmounted(() => {
  stopTicking()
})
</script>
