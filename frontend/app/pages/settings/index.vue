<template>
  <div class="space-y-8 font-sans max-w-2xl mx-auto text-[#e3e2e2]">
    <!-- Title Block Header -->
    <div>
      <h2 class="font-display text-3xl font-bold text-white tracking-tight md:text-4xl">
        Command Settings
      </h2>
      <p class="text-xs text-gray-400 mt-2">
        Adjust portal profile settings, swap active roles, and edit metadata nodes on PortalX commands.
      </p>
    </div>

    <!-- Active Form Wrapper -->
    <div class="bg-[#171717] border border-white/[0.08] p-6 lg:p-8 rounded-xl">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        
        <!-- Avatar Modifier Row -->
        <div class="flex flex-col sm:flex-row items-center gap-6 pb-6 border-b border-white/5">
          <div class="w-16 h-16 rounded-full border border-[#bef264]/20 overflow-hidden shrink-0 bg-[#1e2020] flex items-center justify-center font-bold text-xl text-[#bef264]">
            <img v-if="avatar" :src="avatar" :alt="name" class="w-full h-full object-cover" />
            <span v-else>{{ getInitials(name) }}</span>
          </div>
          <div class="flex-grow space-y-2 w-full">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Avatar Image URL (Logo)</label>
            <input
              v-model="avatar"
              type="text"
              placeholder="Enter photo image URL links..."
              class="w-full bg-[#1e2020] text-xs text-white rounded-lg p-2.5 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none font-mono"
              :disabled="saving"
            />
          </div>
        </div>

        <!-- Name & Email Rows -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Full Name</label>
            <input
              v-model="name"
              type="text"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none"
              :disabled="saving"
            />
          </div>

          <div class="space-y-1">
            <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Email Address</label>
            <input
              v-model="email"
              type="email"
              required
              class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none opacity-60 cursor-not-allowed"
              disabled
              title="Email cannot be changed directly"
            />
          </div>
        </div>

        <!-- Role Selector Option dropdowns -->
        <div class="space-y-1">
          <label class="font-mono text-xs text-gray-400 block uppercase tracking-wider">Active Workspace View Role</label>
          <select
            v-model="role"
            class="w-full bg-[#1e2020] text-white rounded-lg p-3 border border-white/5 focus:ring-1 focus:ring-[#bef264] outline-none text-xs"
            :disabled="saving"
          >
            <option value="Manager">Manager Dashboard View (Total Oversight)</option>
            <option value="Client">Client Portal Billing View (Alex Sterling / Nexus)</option>
          </select>
        </div>

        <!-- Notification Preferences Section -->
        <div class="space-y-4 pt-4 border-t border-white/5">
          <div>
            <h3 class="font-bold text-white">Email Notifications</h3>
            <p class="text-xs text-gray-400 mt-1">Choose which notifications you receive via email.</p>
          </div>
          
          <div class="space-y-3">
            <div class="flex items-center justify-between" v-for="(label, key) in availablePrefs" :key="key">
              <span class="text-sm text-gray-300">{{ label }}</span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" :checked="getPref(key)" @change="togglePref(key)" class="sr-only peer" :disabled="saving">
                <div class="w-9 h-5 bg-[#1e2020] peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-gray-400 peer-checked:after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#bef264]"></div>
              </label>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-4">
          <button
            type="submit"
            :disabled="saving"
            class="px-6 py-3.5 bg-[#bef264] text-[#121c00] hover:bg-[#bef264]/80 font-bold rounded-lg cursor-pointer transform active:scale-95 duration-100 uppercase tracking-wider font-mono text-xs flex items-center justify-center gap-2 border-none outline-none disabled:opacity-50"
          >
            <span v-if="saving" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
            <span>{{ saving ? 'Saving changes...' : 'Save Configuration' }}</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Disconnect / Logout Danger Zone Gateway -->
    <div class="bg-red-500/[0.02] border border-red-500/15 p-6 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="space-y-1 max-w-md text-center sm:text-left">
        <span class="font-mono text-[9px] text-red-400 uppercase tracking-widest font-extrabold">Danger zone actions</span>
        <h4 class="font-display font-semibold text-lg text-white">Disconnect Session</h4>
        <p class="text-xs text-gray-400 leading-relaxed">
          Logs out your active session and locks down access credentials on index modules. Requires secure email passcode.
        </p>
      </div>
      <button
        @click="handleLogoutClick"
        class="bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white font-bold font-mono text-xs px-5 py-3 rounded-lg transition-all cursor-pointer uppercase tracking-wider active:scale-95 text-center shrink-0 border-none outline-none"
      >
        Logout Gate
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from '#app'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'

const authStore = useAuthStore()
const router = useRouter()
const api = useApi()

// Reactive Form Inputs initialized from authStore
const name = ref(authStore.user?.full_name || '')
const email = ref(authStore.user?.email || '')
const avatar = ref(authStore.user?.logo_url || '')
const role = ref('Manager')
const notificationPrefs = ref(authStore.user?.notification_email_prefs || {})
const saving = ref(false)

const availablePrefs = {
  "deliverable_approved": "Deliverable Approved",
  "change_requested": "Change Requested",
  "form_submitted": "Form Submitted",
  "message_received": "Message Received",
  "invoice_paid": "Invoice Paid"
}

const getPref = (key) => {
  return notificationPrefs.value[key] !== false
}

const togglePref = (key) => {
  notificationPrefs.value[key] = !getPref(key)
}

const getInitials = (n) => {
  if (!n) return '?'
  return n.split(' ').map((p) => p[0]).join('').slice(0, 2).toUpperCase()
}

const handleSubmit = async () => {
  saving.value = true

  try {
    // Update backend (simulated or real if the endpoint supports it)
    await api('/api/v1/users/me', {
      method: 'PATCH',
      body: { 
        full_name: name.value, 
        logo_url: avatar.value,
        notification_email_prefs: notificationPrefs.value
      }
    })
    
    // Update local store explicitly
    authStore.user.full_name = name.value
    authStore.user.logo_url = avatar.value
    authStore.user.notification_email_prefs = notificationPrefs.value
    
    alert('Profile configurations updated successfully across high-performance nodes!')
  } catch (err) {
    console.error('Failed to update profile', err)
    alert('Failed to update profile configurations.')
  } finally {
    saving.value = false
  }
}

const handleLogoutClick = () => {
  if (confirm('Are you absolutely sure you want to sign out of PortalX?')) {
    authStore.logout()
    router.push('/auth/login')
  }
}

onMounted(() => {
  // If user data takes a moment to hydrate
  if (authStore.user) {
    name.value = authStore.user.full_name || ''
    email.value = authStore.user.email || ''
    avatar.value = authStore.user.logo_url || ''
    notificationPrefs.value = authStore.user.notification_email_prefs || {}
  }
})
</script>
