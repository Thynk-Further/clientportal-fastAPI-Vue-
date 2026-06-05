<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    <!-- Decorative pulse glow -->
    <section class="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
          Welcome back, {{ authStore.user?.full_name?.split(' ')[0] || 'User' }}
        </h2>
        <p class="text-sm text-gray-400 mt-2 max-w-xl">
          Your projects are currently on track. You have 3 pending tasks requiring your attention today.
        </p>
      </div>
      <div class="flex items-center gap-2 text-gray-400 bg-[#1e2020] px-4 py-2 rounded-full border border-white/[0.03] select-none self-start md:self-auto">
        <span class="relative flex h-2.5 w-2.5">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#bef264] opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#bef264]"></span>
        </span>
        <span class="font-mono text-xs uppercase tracking-wider">System Status: Optimal</span>
      </div>
    </section>

    <!-- Loading State -->
    <div v-if="isLoading" class="animate-pulse space-y-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl h-24"></div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div class="lg:col-span-8 bg-[#171717] h-64 rounded-xl"></div>
        <div class="lg:col-span-4 bg-[#171717] h-64 rounded-xl"></div>
      </div>
    </div>

    <template v-else>
      <!-- Stat Summaries Row -->
      <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col gap-1 transition-all hover:border-[#bef264]/30">
          <span class="font-mono text-[11px] text-gray-400 uppercase tracking-widest">Total Projects</span>
          <div class="flex items-baseline gap-2 mt-2">
            <span class="text-4xl font-extrabold text-white">{{ projects.length }}</span>
            <span class="text-[#bef264] text-xs font-semibold">{{ activeProjects.length }} Active</span>
          </div>
        </div>

        <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col gap-1 transition-all hover:border-[#bef264]/30">
          <span class="font-mono text-[11px] text-gray-400 uppercase tracking-widest">Outstanding Invoices</span>
          <div class="flex items-baseline gap-2 mt-2">
            <span class="text-4xl font-extrabold text-white">${{ outstandingSum.toLocaleString(undefined, {minimumFractionDigits: 2}) }}</span>
            <span class="text-red-400 text-xs font-semibold">{{ outstandingInvoices.length }} Pending</span>
          </div>
        </div>

        <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col gap-1 transition-all hover:border-[#bef264]/30">
          <span class="font-mono text-[11px] text-gray-400 uppercase tracking-widest">Recent Messages</span>
          <div class="flex items-baseline gap-2 mt-2">
            <span class="text-4xl font-extrabold text-white">07</span>
            <span class="text-[#bef264] text-xs font-semibold">3 New</span>
          </div>
        </div>
      </section>

      <!-- Bento Board Row -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Left Bento: Active Projects & Recent Invoices -->
        <div class="lg:col-span-8 space-y-8">
          
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-display text-xl font-bold flex items-center gap-2 text-white">
                <span class="material-symbols-outlined text-[#bef264]">rocket_launch</span>
                Active Projects
              </h3>
              <NuxtLink to="/projects" class="text-[#bef264] font-semibold text-sm hover:underline cursor-pointer">
                View All
              </NuxtLink>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="(project, idx) in activeProjects" :key="project.id" class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden flex flex-col transition-all hover:border-[#bef264]/20">
                <div class="p-6 flex-1">
                  <div class="flex justify-between items-start mb-4 gap-2">
                    <div class="bg-[#bef264]/10 p-2 rounded-lg text-[#bef264] shrink-0">
                      <span class="material-symbols-outlined text-lg leading-none">
                        {{ idx === 0 ? 'architecture' : 'database' }}
                      </span>
                    </div>
                    <span class="px-3 py-1 bg-[#1e2020] text-[#bef264] text-[9px] font-mono rounded-full border border-[#bef264]/20 uppercase tracking-tight text-right select-none truncate">
                      PHASE {{ idx === 0 ? '02: DEVELOPMENT' : '04: QA' }}
                    </span>
                  </div>

                  <h4 class="font-display text-lg font-bold text-white mb-1 truncate">{{ project.name }}</h4>
                  <p class="text-sm text-gray-400 line-clamp-2 h-10">{{ project.description || 'No description provided.' }}</p>

                  <div class="mt-6 space-y-2">
                    <div class="flex justify-between text-[11px] font-mono text-gray-400">
                      <span>PROGRESS</span>
                      <span>{{ project.progress || 25 }}%</span>
                    </div>
                    <div class="w-full bg-[#1e2020] h-1.5 rounded-full overflow-hidden">
                      <div class="bg-[#bef264] h-full rounded-full transition-all duration-500" :style="{ width: `${project.progress || 25}%` }"></div>
                    </div>
                  </div>
                </div>

                <div class="border-t border-white/5 p-4 bg-white/[0.01]">
                  <NuxtLink :to="`/projects/${project.id}`" class="w-full py-2.5 rounded-lg text-sm font-semibold bg-[#2a2d2d] hover:bg-[#343535] text-white transition-colors flex items-center justify-center gap-2 cursor-pointer active:scale-95 transform duration-100">
                    View Details
                    <span class="material-symbols-outlined text-sm leading-none">arrow_forward</span>
                  </NuxtLink>
                </div>
              </div>

              <!-- Empty state for projects if none active -->
              <div v-if="activeProjects.length === 0" class="col-span-1 md:col-span-2 bg-[#171717] border border-dashed border-white/10 rounded-xl p-8 text-center text-gray-400">
                No active projects right now.
              </div>
            </div>
          </div>

          <!-- Recent Invoices list -->
          <div class="space-y-4">
            <h3 class="font-display text-xl font-bold text-white flex items-center gap-2">
              <span class="material-symbols-outlined text-[#bef264]">payments</span>
              Recent Invoices
            </h3>
            <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden overflow-x-auto custom-scrollbar">
              <table class="w-full text-left text-sm border-collapse min-w-[500px]">
                <thead class="bg-[#1e2020] border-b border-white/5 text-gray-400 uppercase tracking-wider font-mono text-xs">
                  <tr>
                    <th class="px-6 py-4">Invoice ID</th>
                    <th class="px-6 py-4">Date</th>
                    <th class="px-6 py-4 text-right">Amount</th>
                    <th class="px-6 py-4 text-center">Status</th>
                    <th class="px-6 py-4"></th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-white/5 font-sans">
                  <tr v-for="inv in invoices.slice(0, 3)" :key="inv.id" class="hover:bg-white/[0.01] transition-colors">
                    <td class="px-6 py-4 font-mono text-white font-medium">{{ inv.stripe_invoice_id || 'Draft' }}</td>
                    <td class="px-6 py-4 text-gray-400">{{ new Date(inv.created_at).toLocaleDateString() }}</td>
                    <td class="px-6 py-4 text-right font-bold text-white">${{ (inv.amount_cents / 100).toLocaleString(undefined, {minimumFractionDigits: 2}) }}</td>
                    <td class="px-6 py-4">
                      <div class="flex justify-center">
                        <span :class="`px-3 py-1 rounded-full text-[10px] font-bold border uppercase tracking-tighter flex items-center gap-1.5 ${
                          inv.status === 'paid' 
                            ? 'bg-green-500/10 text-green-400 border-green-500/20' 
                            : 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
                        }`">
                          <span :class="`h-1.5 w-1.5 rounded-full ${inv.status === 'paid' ? 'bg-green-400' : 'bg-yellow-400'}`"></span>
                          {{ inv.status }}
                        </span>
                      </div>
                    </td>
                    <td class="px-6 py-4 text-right">
                      <button 
                        @click="handleDownload(inv.id, $event)"
                        :disabled="copiedInvoiceId === inv.id"
                        class="text-gray-400 hover:text-[#bef264] transition-colors cursor-pointer p-1.5 rounded-md hover:bg-[#1e2020]"
                        title="Download Invoice"
                      >
                        <span class="material-symbols-outlined text-lg leading-none">
                          {{ copiedInvoiceId === inv.id ? 'check' : 'download' }}
                        </span>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="invoices.length === 0">
                    <td colspan="5" class="px-6 py-8 text-center text-gray-400">No recent invoices found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- Right Bento: Messages & Urgent Contact support -->
        <div class="lg:col-span-4 space-y-8">
          
          <!-- Recent Messages Preview Panel -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-display text-xl font-bold text-white flex items-center gap-2">
                <span class="material-symbols-outlined text-[#bef264]">chat</span>
                Messages
              </h3>
              <span class="bg-[#bef264] text-[#131f00] text-[10px] font-extrabold px-2 py-0.5 rounded uppercase tracking-wider select-none font-mono">
                3 NEW
              </span>
            </div>

            <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden divide-y divide-white/5">
              
              <NuxtLink to="/messages" class="p-4 hover:bg-white/[0.02] cursor-pointer transition-colors group flex flex-col gap-2 block">
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-full bg-[#1e2020] border border-[#bef264]/20 flex items-center justify-center overflow-hidden shrink-0">
                    <img alt="Sarah Jenkins" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCuLoGROHqkSW0wUWeq2IuQ2zovmeKrNfhB5ZO2PCUVuEXUYaqkRl7kzSGHguGKQa29mf-RUfnFdGkqfBRbk7Y61qubsZPG9htSzFleM31D2M38KsjY7wy0N7EuCVonXNJ83CgKMR9ObTvvC3j7G_aN0rpd_v5kX0nLy014P9gWWfKMEFQWOOi71cIDUgKyUD90PhuEP2y1m6lsE9LfCCANLLHdHuRyvyeqFGnTAAxAg7tLI-jUZoHuy6Ns9XPIH7zg0U44iaQ-" class="w-full h-full object-cover" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <h5 class="font-bold text-white text-sm group-hover:text-[#bef264] transition-colors truncate">
                      Sarah Jenkins
                    </h5>
                    <p class="text-[10px] font-mono text-gray-400 uppercase tracking-wider truncate">
                      Account Manager
                    </p>
                  </div>
                  <span class="text-[10px] text-gray-400 shrink-0 font-mono">2h ago</span>
                </div>
                <p class="text-xs text-gray-400 line-clamp-2 italic">
                  "The design team has finished the initial mockups for the Aether dashboard. Can we hop on a quick..."
                </p>
              </NuxtLink>

              <NuxtLink to="/messages" class="p-4 hover:bg-white/[0.02] cursor-pointer transition-colors group flex flex-col gap-2 block">
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-full bg-[#1e2020] border border-white/5 flex items-center justify-center overflow-hidden shrink-0">
                    <img alt="Dev support" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAFytdrTEbAjckvfHVjmHjqPX63U9da6ZRjCqh8ZMCpVISPIiMMTmCvk4bHhM9fCxZ8L1Ooxez1g-9BsfwxnbxgUozoxOuCbdSZbizmcODwPk3-vUdxE2TFt-Tol9UFUw6ECIEjP60qyvyJrtpzs84Run2uPS9hqHtOn8SiKR-DJtCKoyMKMbdoQ1y0FVk4ZKeRQjro_CffVQS1QMuGsgzix-iUMinW1zPBvTXGHiVrhf08ptzchmEElX1ynjoxKSnRWgOhoXGB" class="w-full h-full object-cover" />
                  </div>
                  <div class="flex-1 min-w-0 font-sans">
                    <h5 class="font-bold text-white text-sm group-hover:text-[#bef264] transition-colors truncate">
                      Dev-Support
                    </h5>
                    <p class="text-[10px] font-mono text-gray-400 uppercase tracking-wider truncate">
                      Technical Lead
                    </p>
                  </div>
                  <span class="text-[10px] text-gray-400 shrink-0 font-mono">Yesterday</span>
                </div>
                <p class="text-xs text-gray-400 line-clamp-2 italic">
                  "The latency issue on the EU nodes has been resolved. Please check the monitoring board for..."
                </p>
              </NuxtLink>

              <NuxtLink to="/messages" class="w-full py-4 block text-center text-sm font-bold text-[#bef264] hover:bg-white/[0.02] cursor-pointer transition-colors uppercase tracking-wider">
                Open Chat Dashboard
              </NuxtLink>
            </div>
          </div>

          <!-- Direct Support Scheduler CTA Box -->
          <div class="bg-[#bef264]/[0.04] border border-[#bef264]/20 p-6 rounded-xl flex flex-col">
            <h4 class="font-display font-semibold text-[#bef264] text-lg mb-2">Need immediate assistance?</h4>
            <p class="text-sm text-gray-400 mb-6 font-sans">
              Your dedicated partner team is available for a direct session to review milestones and design sprints.
            </p>
            <div class="space-y-3">
              <button @click="showCallModal = true" class="w-full bg-white text-[#121414] hover:bg-[#bef264] hover:text-[#131f00] py-3 rounded-lg font-bold active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer uppercase tracking-wider font-mono text-xs">
                <span class="material-symbols-outlined text-sm">calendar_today</span>
                Schedule Call
              </button>
              <button @click="showEmailModal = true" class="w-full bg-[#1e2020] text-white hover:bg-[#212323] py-3 rounded-lg font-bold active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer border border-white/5 uppercase tracking-wider font-mono text-xs">
                <span class="material-symbols-outlined text-sm">mail</span>
                Send Email
              </button>
            </div>
          </div>

        </div>
      </div>
    </template>

    <!-- SCHEDULE CALL MODAL -->
    <div v-if="showCallModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-6 max-w-sm w-full space-y-4">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-lg font-bold text-white">Schedule Call Session</h4>
          <button @click="showCallModal = false" class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer">close</button>
        </div>
        <p class="text-sm text-gray-400 leading-relaxed font-sans">
          Book a direct meeting with your Lead Account partners. Choose a perfect slot in our calendar list.
        </p>
        <div class="space-y-2 text-sm font-mono">
          <button @click="selectSlot" class="w-full text-left p-3 rounded-lg bg-[#212323] text-[#e3e2e2] hover:bg-[#bef264] hover:text-[#121414] transition-all">
            🗓️ Monday, 10:00 AM EST (Available)
          </button>
          <button @click="selectSlot" class="w-full text-left p-3 rounded-lg bg-[#212323] text-[#e3e2e2] hover:bg-[#bef264] hover:text-[#121414] transition-all">
            🗓️ Wednesday, 2:30 PM EST (Available)
          </button>
        </div>
      </div>
    </div>

    <!-- SEND EMAIL QUICK MODAL -->
    <div v-if="showEmailModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-6 max-w-md w-full space-y-4">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-lg font-bold text-white">Compose Message</h4>
          <button @click="showEmailModal = false" class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer">close</button>
        </div>
        <div class="space-y-3 font-sans">
          <div>
            <label class="text-xs text-gray-400 block uppercase tracking-wider font-mono mb-1">To</label>
            <div class="bg-[#1e2020] text-white rounded-lg p-2.5 border border-white/5">
              Sarah Jenkins & Dev team
            </div>
          </div>
          <div>
            <label class="text-xs text-gray-400 block uppercase tracking-wider font-mono mb-1">Subject</label>
            <input type="text" value="PortalX Project Milestone Review" class="w-full bg-[#1e2020] text-white rounded-lg p-2.5 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none" />
          </div>
          <div>
            <label class="text-xs text-gray-400 block uppercase tracking-wider font-mono mb-1">Message Body</label>
            <textarea rows="4" placeholder="Type your message here..." class="w-full bg-[#1e2020] text-white rounded-lg p-2.5 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none resize-none text-xs" />
          </div>
        </div>
        <div class="flex justify-end gap-2 text-sm pt-2">
          <button @click="showEmailModal = false" class="px-4 py-2 hover:bg-white/[0.05] rounded-lg">Cancel</button>
          <button @click="sendEmail" class="px-5 py-2 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'

const authStore = useAuthStore()
const api = useApi()

const projects = ref([])
const invoices = ref([])
const isLoading = ref(true)

const activeProjects = computed(() => {
  return projects.value.filter(p => p.status === 'active' || p.status === 'In Progress').slice(0, 2)
})

const outstandingInvoices = computed(() => {
  return invoices.value.filter(inv => inv.status === 'pending' || inv.status === 'overdue' || inv.status === 'sent')
})

const outstandingSum = computed(() => {
  return outstandingInvoices.value.reduce((sum, inv) => sum + (inv.amount_cents / 100), 0)
})

onMounted(async () => {
  try {
    const [projectsData, invoicesData] = await Promise.all([
      api('/api/v1/projects').catch(() => []),
      api('/api/v1/invoices').catch(() => [])
    ])
    projects.value = projectsData || []
    invoices.value = invoicesData || []
  } catch (error) {
    console.error('Failed to fetch dashboard data', error)
  } finally {
    isLoading.value = false
  }
})

// UI State
const showCallModal = ref(false)
const showEmailModal = ref(false)
const copiedInvoiceId = ref(null)

const handleDownload = (id, e) => {
  e.stopPropagation()
  copiedInvoiceId.value = id
  setTimeout(() => {
    copiedInvoiceId.value = null
    alert(`Invoice ${id} has been compiled and downloaded securely.`)
  }, 1500)
}

const selectSlot = () => {
  alert('Slot selected!')
  showCallModal.value = false
}

const sendEmail = () => {
  alert('Message sent successfully!')
  showEmailModal.value = false
}
</script>
