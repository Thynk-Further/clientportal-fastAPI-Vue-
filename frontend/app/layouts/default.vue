<template>
  <div class="min-h-screen bg-gray-50 flex font-sans">
    <!-- Sidebar Navigation -->
    <aside class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col shadow-sm relative z-10">
      <div class="p-6">
        <!-- Temporary logo placeholder -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-md">
            <span class="text-white font-bold text-sm">CP</span>
          </div>
          <h1 class="text-xl font-bold text-gray-900 tracking-tight">ClientPortal</h1>
        </div>
      </div>
      
      <!-- Navigation Links -->
      <nav class="mt-2 px-4 space-y-1 flex-1">
        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4 px-2 mt-4">Dashboard</p>
        
        <!-- NuxtLink automatically adds 'router-link-active' classes when you are on that route! -->
        <NuxtLink to="/" class="flex items-center gap-3 px-3 py-2.5 text-sm font-medium rounded-lg transition-colors"
                  active-class="bg-indigo-50 text-indigo-700"
                  exact-active-class="bg-indigo-50 text-indigo-700"
                  :class="[$route.path === '/' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
          <LayoutDashboard class="w-5 h-5" />
          Overview
        </NuxtLink>

        <NuxtLink to="/clients" class="flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-lg transition-colors"
                  active-class="bg-indigo-50 text-indigo-700">
          <Users class="w-5 h-5" />
          Clients
        </NuxtLink>

        <NuxtLink to="/projects" class="flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-lg transition-colors"
                  active-class="bg-indigo-50 text-indigo-700">
          <FolderKanban class="w-5 h-5" />
          Projects
        </NuxtLink>
      </nav>

      <!-- User Profile & Logout Bottom Section -->
      <div class="p-4 border-t border-gray-100 bg-gray-50/50">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3 truncate">
            <!-- Dynamically grab the first letter of the user's name, or 'U' if not loaded yet -->
            <div class="w-9 h-9 rounded-full bg-indigo-100 flex shrink-0 items-center justify-center text-indigo-700 font-bold text-sm shadow-inner border border-indigo-200">
              {{ authStore.user?.full_name ? authStore.user.full_name.charAt(0).toUpperCase() : 'U' }}
            </div>
            <div class="truncate">
              <!-- Dynamically show their full name and tier -->
              <p class="text-sm font-medium text-gray-900 truncate">{{ authStore.user?.full_name || 'Loading...' }}</p>
              <p class="text-xs text-gray-500 uppercase tracking-wider font-semibold">{{ authStore.user?.subscription_tier || 'FREE' }} PLAN</p>
            </div>
          </div>
          
          <!-- Logout Button -->
          <button @click="handleLogout" class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors" title="Log out">
            <LogOut class="w-5 h-5" />
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Mobile Header -->
      <header class="bg-white border-b border-gray-200 h-16 flex items-center px-6 justify-between md:hidden shadow-sm z-20 relative">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-md">
            <span class="text-white font-bold text-sm">CP</span>
          </div>
          <span class="font-bold text-gray-900">ClientPortal</span>
        </div>
        <button @click="handleLogout" class="text-gray-500 hover:text-red-600 p-2">
          <LogOut class="w-5 h-5" />
        </button>
      </header>
      
      <!-- Where the nested pages are injected -->
      <main class="flex-1 overflow-y-auto bg-gray-50 p-4 md:p-8">
        <!-- slot is where pages/index.vue will be rendered! -->
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
/**
 * Setup script for the dashboard layout.
 */
import { useRouter, useRoute } from '#app'
import { useAuthStore } from '~/stores/auth'
// Import awesome icons from lucide-vue-next
import { LayoutDashboard, Users, FolderKanban, LogOut } from 'lucide-vue-next'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

/**
 * Handle logging out
 */
const handleLogout = () => {
  authStore.logout()
  router.push('/auth/login')
}
</script>
