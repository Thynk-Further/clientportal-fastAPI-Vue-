<template>
  <div class="bg-[#121414] text-[#e3e2e2] min-h-screen flex font-sans antialiased text-sm">
    <!-- PERSISTENT LEFT SIDEBAR PANEL (Desktop-Only) -->
    <aside class="w-64 border-r border-white/5 bg-[#121414] flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none hidden md:flex z-10">
      <div class="flex flex-col gap-8 py-6">
        <!-- Logo container -->
        <div class="px-6 flex items-center gap-2.5 font-display font-black text-lg tracking-tight text-white">
          <span class="material-symbols-outlined text-[#bef264] text-xl">account_tree</span>
          PortalX
        </div>

        <!-- Tab Navigation items -->
        <nav class="px-3 space-y-1.5 flex flex-col font-sans text-xs">
          <!-- Overview Dashboard -->
          <NuxtLink
            to="/"
            class="flex items-center gap-3.5 px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
            exact-active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <span class="material-symbols-outlined text-md leading-none">home_app_logo</span>
            Overview Dashboard
          </NuxtLink>

          <!-- Workspace Projects -->
          <NuxtLink
            to="/projects"
            class="flex items-center gap-3.5 px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <span class="material-symbols-outlined text-md leading-none">rocket_launch</span>
            Workspace Projects
          </NuxtLink>

          <!-- Client Connections -->
          <NuxtLink
            to="/clients"
            class="flex items-center gap-3.5 px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <span class="material-symbols-outlined text-md leading-none">handshake</span>
            Client Connections
          </NuxtLink>

          <!-- Time & Work Ledger -->
          <NuxtLink
            to="/time-tracking"
            class="flex items-center gap-3.5 px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <span class="material-symbols-outlined text-md leading-none">timer</span>
            Time & Work Ledger
          </NuxtLink>

          <!-- Forms & Questionnaires -->
          <NuxtLink
            to="/forms"
            class="flex items-center gap-3.5 px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <span class="material-symbols-outlined text-md leading-none">dynamic_form</span>
            Forms & Questionnaires
          </NuxtLink>

          <!-- Invoices & Billing Account -->
          <NuxtLink
            to="/invoices"
            class="flex items-center gap-3.5 px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <span class="material-symbols-outlined text-md leading-none">payments</span>
            Invoices & Billing
          </NuxtLink>

          <!-- Support Messaging Panel -->
          <NuxtLink
            to="/messages"
            class="flex items-center justify-between px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <div class="flex items-center gap-3.5">
              <span class="material-symbols-outlined text-md leading-none">chat</span>
              Support Messaging
            </div>
            <!-- <span class="h-2 w-2 rounded-full bg-[#bef264] animate-pulse"></span> -->
          </NuxtLink>

          <!-- Notifications -->
          <button
            @click="isNotificationsOpen = true"
            class="flex items-center justify-between w-full px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
          >
            <div class="flex items-center gap-3.5">
              <span class="material-symbols-outlined text-md leading-none">notifications</span>
              Notifications
            </div>
            <span v-if="unreadCount > 0" class="bg-[#bef264] text-[#131f00] text-[10px] px-1.5 py-0.5 rounded-full font-black">
              {{ unreadCount }}
            </span>
          </button>

          <!-- Command Settings -->
          <NuxtLink
            to="/settings"
            class="flex items-center gap-3.5 px-4.5 py-3 rounded-lg font-bold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.01]"
            active-class="bg-white/[0.05] !text-[#bef264] hover:!text-[#bef264]"
          >
            <span class="material-symbols-outlined text-md leading-none">settings</span>
            Command Settings
          </NuxtLink>
        </nav>
      </div>

      <!-- Global User Profile block drawer -->
      <div class="p-4 border-t border-white/5 space-y-4 font-sans bg-[#171717]/30">
        <div class="flex items-center gap-3">
          <div class="h-10 w-10 rounded-full border border-white/5 overflow-hidden shrink-0 bg-[#1e2020] flex items-center justify-center text-[#bef264] font-bold">
            {{ authStore.user?.full_name ? authStore.user.full_name.charAt(0).toUpperCase() : 'U' }}
          </div>
          <div class="min-w-0 flex-1">
            <h5 class="font-bold text-white text-xs truncate leading-tight">{{ authStore.user?.full_name || 'Loading...' }}</h5>
            <span class="text-[10px] font-mono tracking-wider font-extrabold text-[#bef264] uppercase select-none leading-none block mt-1">
              {{ authStore.user?.subscription_tier || 'FREE' }} PLAN
            </span>
          </div>
        </div>

        <!-- Quick Dual Role Changer widget -->
        <button
          @click="handleLogout"
          class="w-full py-2 bg-white/5 hover:bg-red-500/10 hover:text-red-400 text-gray-400 rounded text-[10px] font-bold font-mono transition-all flex items-center justify-center gap-1.5 cursor-pointer uppercase tracking-wider border-none"
          title="Log out of session"
        >
          <span class="material-symbols-outlined text-xs leading-none">logout</span>
          <span>Logout</span>
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT LOADING GRID FRAME -->
    <div class="flex-grow flex flex-col min-w-0 max-h-screen overflow-y-auto bg-[#121414]">
      
      <!-- MOBILE NAVIGATION HEADER -->
      <header class="md:hidden flex justify-between items-center px-6 h-16 bg-[#121414] border-b border-white/5 z-40 sticky top-0">
        <div class="font-display font-black text-lg text-white flex items-center gap-2">
          <span class="material-symbols-outlined text-[#bef264] text-lg">account_tree</span>
          PortalX
        </div>
        <div class="flex items-center gap-4 font-mono text-xs">
          <button @click="isNotificationsOpen = true" class="text-gray-400 hover:text-white relative mt-1">
            <span class="material-symbols-outlined text-[20px]">notifications</span>
            <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-[#bef264] rounded-full border-2 border-[#121414]"></span>
          </button>
          <button
            @click="handleLogout"
            class="px-2.5 py-1 text-[10px] uppercase font-bold border border-white/10 rounded bg-[#1e2020] text-gray-400 hover:text-red-400"
          >
            Logout
          </button>
        </div>
      </header>

      <!-- Notification Slide-over -->
      <NotificationSlideover
        :is-open="isNotificationsOpen"
        :is-portal="false"
        @close="isNotificationsOpen = false"
        @update:unreadCount="count => unreadCount = count"
      />

      <!-- Dynamic active views dispatcher -->
      <main class="flex-grow p-6 md:p-8 lg:p-10 pb-24 md:pb-12">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useNuxtApp } from '#app'
import { useAuthStore } from '~/stores/auth'
import { ref, onMounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const isNotificationsOpen = ref(false)
const unreadCount = ref(0)

const handleLogout = () => {
  authStore.logout()
  router.push('/auth/login')
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    try {
      const { $api } = useNuxtApp()
      const res = await $api('/api/v1/notifications?limit=1')
      unreadCount.value = res.unread_count
    } catch (err) {
      console.error('Failed to fetch initial unread count', err)
    }
  }
})
</script>
