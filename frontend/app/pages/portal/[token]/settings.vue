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
            <div class="relative w-20 h-20 rounded-full border border-white/10 bg-[#1e2020] overflow-hidden shrink-0 flex items-center justify-center font-bold text-xl text-[#bef264] group">
              <img v-if="me?.avatar_url" :src="me.avatar_url" class="w-full h-full object-cover" />
              <span v-else>{{ me?.name ? me.name.substring(0, 2).toUpperCase() : 'ME' }}</span>
              
              <label v-if="me?.role === 'primary'" class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center cursor-pointer transition-opacity">
                <input type="file" class="hidden" accept="image/*" @change="handleAvatarUpload" />
                <span class="material-symbols-outlined text-white text-sm" v-if="!isUploadingAvatar">upload</span>
                <span class="material-symbols-outlined text-white text-sm animate-spin" v-else>progress_activity</span>
              </label>
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
            <div class="space-y-2" v-if="me?.role === 'primary'">
              <label class="text-xs text-gray-400 font-mono uppercase tracking-widest block">Phone Number</label>
              <input type="text" :value="me?.phone || 'Not provided'" disabled class="w-full bg-[#1e2020]/50 border border-white/5 rounded-lg p-3 text-sm text-gray-500 cursor-not-allowed" />
            </div>
            <div class="space-y-2" v-if="me?.role === 'primary'">
              <label class="text-xs text-gray-400 font-mono uppercase tracking-widest block">Address</label>
              <input type="text" :value="me?.address || 'Not provided'" disabled class="w-full bg-[#1e2020]/50 border border-white/5 rounded-lg p-3 text-sm text-gray-500 cursor-not-allowed" />
            </div>
          </div>
          <p v-if="me?.role === 'primary'" class="text-xs text-gray-500 italic mt-2">
            Contact information is managed by your freelancer. Please contact them to update these details.
          </p>

        </div>
      </section>

      <!-- Notification Preferences Section -->
      <section v-if="me?.role === 'primary'" class="bg-[#171717] border border-white/5 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#1e2020]/50">
          <div>
            <h2 class="font-bold text-white text-lg">Email Notifications</h2>
            <p class="text-xs text-gray-400 mt-1">Choose which email notifications you receive.</p>
          </div>
        </div>
        
        <div class="divide-y divide-white/5">
          <div class="px-6 py-4 flex items-center justify-between" v-for="(label, key) in availablePrefs" :key="key">
            <div class="flex items-center gap-3">
              <div>
                <h4 class="text-sm text-white">{{ label }}</h4>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" :checked="getPref(key)" @change="togglePref(key)" class="sr-only peer">
              <div class="w-9 h-5 bg-[#1e2020] peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-gray-400 peer-checked:after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#bef264]"></div>
            </label>
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
const isUploadingAvatar = ref(false)

const availablePrefs = {
  "deliverable_uploaded": "New Deliverables",
  "message_received": "New Messages"
}

const getPref = (key) => {
  if (!me.value || !me.value.notification_email_prefs) return true
  return me.value.notification_email_prefs[key] !== false
}

const togglePref = async (key) => {
  const current = getPref(key)
  const newPrefs = { ...(me.value.notification_email_prefs || {}) }
  newPrefs[key] = !current
  
  try {
    const res = await api('/api/v1/portal/me/notification-preferences', {
      method: 'PATCH',
      body: { prefs: newPrefs }
    })
    me.value.notification_email_prefs = res.prefs
  } catch (error) {
    console.error('Failed to update prefs', error)
  }
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  isUploadingAvatar.value = true
  try {
    const { presigned_url, object_key } = await api('/api/v1/portal/me/avatar/presigned-url', {
      method: 'POST',
      body: { filename: file.name, content_type: file.type }
    })

    await fetch(presigned_url, {
      method: 'PUT',
      headers: { 'Content-Type': file.type },
      body: file
    })

    const finalUrl = `https://cdn.clientportal.dev/${object_key}` // Adjust based on R2 public URL
    
    // In dev, if there's no public URL, maybe use object_key. For MVP we'll construct the R2 dev url.
    // Assuming backend returns object_key, we can just save it or construct a public URL.
    // Wait, the backend config settings.R2_PUBLIC_URL isn't explicitly used here, but we can just use a fake domain or the R2 endpoint for now.
    // Actually, we'll patch it with `object_key` and backend could resolve it, but avatar_url expects a full URL.
    const avatarUrl = `https://pub-286a0d4c82ec45eb8038b368ee3df95a.r2.dev/${object_key}`

    const res = await api('/api/v1/portal/me/avatar', {
      method: 'PATCH',
      body: { avatar_url: avatarUrl }
    })
    me.value.avatar_url = res.avatar_url
  } catch (error) {
    console.error('Failed to upload avatar', error)
  } finally {
    isUploadingAvatar.value = false
  }
}

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
