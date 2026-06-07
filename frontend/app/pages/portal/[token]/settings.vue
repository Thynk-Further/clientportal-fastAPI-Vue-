<template>
  <div class="space-y-8 font-sans max-w-4xl mx-auto text-[#e3e2e2]">
    
    <!-- Header -->
    <div class="border-b border-white/5 pb-6">
      <h1 class="font-display text-3xl font-bold tracking-tight text-white mb-2">
        Account Settings
      </h1>
      <p class="text-sm text-gray-400">
        Manage your profile, notification preferences, and team access.
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="animate-pulse space-y-10">
      <div class="bg-[#171717] h-64 rounded-xl border border-white/5"></div>
      <div class="bg-[#171717] h-48 rounded-xl border border-white/5"></div>
    </div>

    <!-- Main Content -->
    <div v-else class="space-y-10">
      
      <!-- Profile Section -->
      <section class="bg-[#171717] border border-white/5 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#1e2020]/50">
          <div>
            <h2 class="font-bold text-white text-lg">Personal Profile</h2>
            <p class="text-xs text-gray-400 mt-1">View your personal information and contact details.</p>
          </div>
        </div>
        
        <div class="p-6 space-y-6">
          <div class="flex items-center gap-6">
            <div class="w-20 h-20 rounded-full border border-white/10 bg-[#1e2020] overflow-hidden shrink-0 flex items-center justify-center font-bold text-xl text-[#bef264]">
              {{ me?.name ? me.name.substring(0, 2).toUpperCase() : 'ME' }}
            </div>
            <div>
              <p class="text-[10px] text-gray-500 font-mono uppercase">{{ me?.role === 'primary' ? 'Primary Account' : 'Team Member' }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-xs text-gray-400 font-mono uppercase tracking-widest block">Full Name</label>
              <input type="text" :value="me?.name" disabled class="w-full bg-[#1e2020]/50 border border-white/5 rounded-lg p-3 text-sm text-gray-500 cursor-not-allowed" />
            </div>
            <div class="space-y-2">
              <label class="text-xs text-gray-400 font-mono uppercase tracking-widest block">Email Address</label>
              <input type="email" :value="me?.email" disabled class="w-full bg-[#1e2020]/50 border border-white/5 rounded-lg p-3 text-sm text-gray-500 cursor-not-allowed" />
            </div>
          </div>
        </div>
      </section>

      <!-- Team Members Section -->
      <section v-if="me?.role === 'primary'" class="bg-[#171717] border border-white/5 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#1e2020]/50">
          <div>
            <h2 class="font-bold text-white text-lg">Team Access</h2>
            <p class="text-xs text-gray-400 mt-1">Manage your team members and their access to this portal.</p>
          </div>
        </div>
        
        <div class="divide-y divide-white/5">
          <div class="px-6 py-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-[#1e2020] border border-white/10 flex items-center justify-center text-white font-bold text-sm">
                {{ me?.name ? me.name.substring(0, 2).toUpperCase() : 'ME' }}
              </div>
              <div>
                <h4 class="text-sm font-bold text-white">{{ me?.name }} <span class="bg-[#bef264]/10 text-[#bef264] px-2 py-0.5 rounded text-[9px] font-mono ml-2 uppercase">Primary</span></h4>
                <p class="text-xs text-gray-500">{{ me?.email }}</p>
              </div>
            </div>
          </div>

          <div v-for="member in teamMembers" :key="member.id" class="px-6 py-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-[#1e2020] border border-white/10 flex items-center justify-center text-gray-400 font-bold text-sm">
                {{ member.name.substring(0, 2).toUpperCase() }}
              </div>
              <div>
                <h4 class="text-sm font-bold text-white">{{ member.name }}</h4>
                <p class="text-xs text-gray-500">{{ member.email }}</p>
              </div>
            </div>
            <button @click="removeMember(member.id)" class="text-gray-500 hover:text-red-400 transition-colors disabled:opacity-50" :disabled="isRemoving">
              <span v-if="removingId === member.id" class="material-symbols-outlined text-[18px] animate-spin">progress_activity</span>
              <span v-else class="material-symbols-outlined text-[18px]">delete</span>
            </button>
          </div>

          <div v-if="teamMembers.length === 0" class="px-6 py-8 text-center text-gray-500 text-sm">
            You haven't invited any team members yet. Invite members from the Dashboard.
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({
  layout: 'portal'
})

const api = useApi()

const me = ref(null)
const teamMembers = ref([])
const isLoading = ref(true)
const isRemoving = ref(false)
const removingId = ref(null)

onMounted(async () => {
  try {
    const meData = await api('/api/v1/portal/me')
    me.value = meData
    
    if (meData?.role === 'primary') {
      const membersData = await api('/api/v1/portal/members')
      teamMembers.value = membersData || []
    }
  } catch (error) {
    console.error('Failed to load settings data', error)
  } finally {
    isLoading.value = false
  }
})

const removeMember = async (memberId) => {
  if (!confirm("Are you sure you want to remove this team member? Their access will be revoked immediately.")) return
  
  isRemoving.value = true
  removingId.value = memberId
  try {
    await api(`/api/v1/portal/members/${memberId}`, { method: 'DELETE' })
    teamMembers.value = teamMembers.value.filter(m => m.id !== memberId)
  } catch (error) {
    console.error('Failed to remove member', error)
    alert(error.data?.detail || 'Failed to remove member.')
  } finally {
    isRemoving.value = false
    removingId.value = null
  }
}
</script>
