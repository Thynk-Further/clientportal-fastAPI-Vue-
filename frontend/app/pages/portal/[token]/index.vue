<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    <!-- Decorative pulse glow -->
    <section class="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
          Secure Client Terminal
        </h2>
        <p class="text-sm text-gray-400 mt-2 max-w-xl">
          Access active development milestones, review architectural deliverables, and collaborate with your project team.
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
          <span class="font-mono text-[11px] text-gray-400 uppercase tracking-widest">Active Questionnaires</span>
          <div class="flex items-baseline gap-2 mt-2">
            <span class="text-4xl font-extrabold text-white">{{ forms.length }}</span>
            <span class="text-[#bef264] text-xs font-semibold">Pending</span>
          </div>
        </div>

        <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col gap-1 transition-all hover:border-[#bef264]/30">
          <span class="font-mono text-[11px] text-gray-400 uppercase tracking-widest">Team Members</span>
          <div class="flex items-baseline gap-2 mt-2">
            <span class="text-4xl font-extrabold text-white">0{{ teamMembers.length }}</span>
            <span class="text-[#bef264] text-xs font-semibold"> / 3 Max</span>
          </div>
        </div>
      </section>

      <!-- Bento Board Row -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Left Bento: Active Projects & Team Members -->
        <div class="lg:col-span-8 space-y-8">
          
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-display text-xl font-bold flex items-center gap-2 text-white">
                <span class="material-symbols-outlined text-[#bef264]">rocket_launch</span>
                Active Projects
              </h3>
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
                      {{ project.status === 'active' ? 'IN PROGRESS' : project.status }}
                    </span>
                  </div>

                  <h4 class="font-display text-lg font-bold text-white mb-1 truncate">{{ project.name }}</h4>
                  <p class="text-sm text-gray-400 line-clamp-2 h-10">{{ project.description || 'No description provided.' }}</p>
                </div>

                <div class="border-t border-white/5 p-4 bg-white/[0.01]">
                  <NuxtLink :to="`/portal/${route.params.token}/projects/${project.id}`" class="w-full py-2.5 rounded-lg text-sm font-semibold bg-[#2a2d2d] hover:bg-[#343535] text-white transition-colors flex items-center justify-center gap-2 cursor-pointer active:scale-95 transform duration-100">
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

          <!-- Team Members -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-display text-xl font-bold text-white flex items-center gap-2">
                <span class="material-symbols-outlined text-[#bef264]">group</span>
                Team Management
              </h3>
              <button @click="showInviteModal = true" :disabled="teamMembers.length >= 3" class="bg-[#bef264] text-[#131f00] text-[10px] font-extrabold px-3 py-1.5 rounded uppercase tracking-wider select-none font-mono cursor-pointer hover:bg-[#a3d64c] transition-colors disabled:opacity-50">
                + Invite Member
              </button>
            </div>
            <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden overflow-x-auto custom-scrollbar">
              <table class="w-full text-left text-sm border-collapse min-w-[500px]">
                <thead class="bg-[#1e2020] border-b border-white/5 text-gray-400 uppercase tracking-wider font-mono text-xs">
                  <tr>
                    <th class="px-6 py-4">Name</th>
                    <th class="px-6 py-4">Email</th>
                    <th class="px-6 py-4">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-white/5 font-sans">
                  <tr v-for="member in teamMembers" :key="member.id" class="hover:bg-white/[0.01] transition-colors">
                    <td class="px-6 py-4 font-bold text-white">{{ member.name }}</td>
                    <td class="px-6 py-4 text-gray-400">{{ member.email }}</td>
                    <td class="px-6 py-4">
                      <span class="px-3 py-1 bg-[#1e2020] text-[#bef264] text-[9px] font-mono rounded-full border border-[#bef264]/20 uppercase tracking-tight">Joined</span>
                    </td>
                  </tr>
                  <tr v-if="teamMembers.length === 0">
                    <td colspan="3" class="px-6 py-8 text-center text-gray-400">No team members invited yet.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- Right Bento: Questionnaires & Support -->
        <div class="lg:col-span-4 space-y-8">
          
          <!-- Recent Questionnaires Preview Panel -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-display text-xl font-bold text-white flex items-center gap-2">
                <span class="material-symbols-outlined text-[#bef264]">dynamic_form</span>
                Questionnaires
              </h3>
            </div>

            <div class="bg-[#171717] border border-white/[0.08] rounded-xl overflow-hidden divide-y divide-white/5">
              
              <NuxtLink v-for="form in forms.slice(0, 3)" :key="form.id" :to="`/portal/${route.params.token}/forms/${form.id}`" class="p-4 hover:bg-white/[0.02] cursor-pointer transition-colors group flex flex-col gap-2 block">
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-full bg-[#1e2020] border border-[#bef264]/20 flex items-center justify-center overflow-hidden shrink-0 text-[#bef264]">
                    <span class="material-symbols-outlined text-lg">receipt_long</span>
                  </div>
                  <div class="flex-1 min-w-0">
                    <h5 class="font-bold text-white text-sm group-hover:text-[#bef264] transition-colors truncate">
                      {{ form.title }}
                    </h5>
                    <p class="text-[10px] font-mono text-gray-400 uppercase tracking-wider truncate">
                      {{ form.status }}
                    </p>
                  </div>
                </div>
              </NuxtLink>

              <div v-if="forms.length === 0" class="p-6 text-center text-gray-400 text-sm">
                No active questionnaires.
              </div>
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

    <!-- INVITE MEMBER MODAL -->
    <div v-if="showInviteModal" class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-[#171717] border border-white/10 rounded-xl p-6 max-w-sm w-full space-y-4">
        <div class="flex justify-between items-start">
          <h4 class="font-display text-lg font-bold text-white">Invite Team Member</h4>
          <button @click="showInviteModal = false" class="material-symbols-outlined text-gray-400 hover:text-[#bef264] p-1 cursor-pointer">close</button>
        </div>
        <p class="text-sm text-gray-400 leading-relaxed font-sans mb-4">
          Invite up to 3 team members to collaborate securely in this portal. They will receive their own magic link.
        </p>
        <div v-if="inviteError" class="p-2 bg-red-500/10 text-red-400 text-xs rounded border border-red-500/20">
          {{ inviteError }}
        </div>
        <div class="space-y-3 font-sans">
          <div>
            <label class="text-xs text-gray-400 block uppercase tracking-wider font-mono mb-1">Full Name</label>
            <input v-model="inviteForm.name" type="text" placeholder="e.g. Jane Doe" class="w-full bg-[#1e2020] text-white rounded-lg p-2.5 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none" />
          </div>
          <div>
            <label class="text-xs text-gray-400 block uppercase tracking-wider font-mono mb-1">Email Address</label>
            <input v-model="inviteForm.email" type="email" placeholder="jane@company.com" class="w-full bg-[#1e2020] text-white rounded-lg p-2.5 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none" />
          </div>
        </div>
        <div class="flex justify-end gap-2 text-sm pt-4">
          <button @click="showInviteModal = false" class="px-4 py-2 hover:bg-white/[0.05] rounded-lg">Cancel</button>
          <button @click="inviteMember" :disabled="isInviting" class="px-5 py-2 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg flex items-center gap-2">
            <span v-if="isInviting" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
            Send Invite
          </button>
        </div>
      </div>
    </div>

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
          <button @click="showCallModal = false" class="w-full text-left p-3 rounded-lg bg-[#212323] text-[#e3e2e2] hover:bg-[#bef264] hover:text-[#121414] transition-all">
            🗓️ Monday, 10:00 AM EST (Available)
          </button>
          <button @click="showCallModal = false" class="w-full text-left p-3 rounded-lg bg-[#212323] text-[#e3e2e2] hover:bg-[#bef264] hover:text-[#121414] transition-all">
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
              Account Manager
            </div>
          </div>
          <div>
            <label class="text-xs text-gray-400 block uppercase tracking-wider font-mono mb-1">Subject</label>
            <input type="text" class="w-full bg-[#1e2020] text-white rounded-lg p-2.5 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none" />
          </div>
          <div>
            <label class="text-xs text-gray-400 block uppercase tracking-wider font-mono mb-1">Message Body</label>
            <textarea rows="4" placeholder="Type your message here..." class="w-full bg-[#1e2020] text-white rounded-lg p-2.5 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none resize-none text-xs" />
          </div>
        </div>
        <div class="flex justify-end gap-2 text-sm pt-2">
          <button @click="showEmailModal = false" class="px-4 py-2 hover:bg-white/[0.05] rounded-lg">Cancel</button>
          <button @click="showEmailModal = false" class="px-5 py-2 hover:bg-[#bef264]/80 bg-[#bef264] text-[#131f00] font-bold rounded-lg">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '~/composables/useApi'

const route = useRoute()
const api = useApi()

const projects = ref([])
const forms = ref([])
const teamMembers = ref([])
const isLoading = ref(true)

const activeProjects = computed(() => {
  return projects.value.filter(p => p.status === 'active' || p.status === 'In Progress').slice(0, 2)
})

onMounted(async () => {
  try {
    const [projectsData, formsData, membersData] = await Promise.all([
      api('/api/v1/portal/projects').catch(() => []),
      api('/api/v1/portal/forms').catch(() => []),
      api('/api/v1/portal/members').catch(() => [])
    ])
    projects.value = projectsData || []
    forms.value = formsData || []
    teamMembers.value = membersData || []
  } catch (error) {
    console.error('Failed to fetch dashboard data', error)
  } finally {
    isLoading.value = false
  }
})

// UI State
const showCallModal = ref(false)
const showEmailModal = ref(false)
const showInviteModal = ref(false)

const inviteForm = ref({ name: '', email: '' })
const isInviting = ref(false)
const inviteError = ref('')

const inviteMember = async () => {
  inviteError.value = ''
  if (!inviteForm.value.name || !inviteForm.value.email) {
    inviteError.value = "Please fill in all fields"
    return
  }
  
  isInviting.value = true
  try {
    const member = await api('/api/v1/portal/members', {
      method: 'POST',
      body: inviteForm.value
    })
    teamMembers.value.push(member)
    showInviteModal.value = false
    inviteForm.value = { name: '', email: '' }
    alert(`Magic link generated for ${member.name}! It would be emailed to ${member.email} in production.`)
  } catch (err) {
    inviteError.value = err.data?.detail || "Failed to invite member."
  } finally {
    isInviting.value = false
  }
}
</script>
