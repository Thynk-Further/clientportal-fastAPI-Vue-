<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    
    <!-- Header -->
    <div class="space-y-2">
      <div class="flex items-center gap-2 text-xs font-mono text-[#bef264] uppercase tracking-wider font-bold mb-4 bg-[#bef264]/10 inline-flex px-2 py-1 rounded-full border border-[#bef264]/20">
        <span class="w-1.5 h-1.5 bg-[#bef264] rounded-full animate-pulse"></span>
        Live Onboarding • Phase 01
      </div>
      <h1 class="font-display text-4xl md:text-5xl font-bold tracking-tight text-white">
        Welcome to the <span class="text-[#bef264]">Command Center.</span>
      </h1>
      <p class="text-gray-400 max-w-2xl text-base pt-2">
        We've configured your environment. Follow this guided walkthrough to synchronize your workflow with PortalX.
      </p>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-4">
      
      <!-- Video Area -->
      <div class="lg:col-span-2 relative bg-[#171717] rounded-xl overflow-hidden border border-white/5 aspect-video group cursor-pointer shadow-lg hover:border-[#bef264]/30 transition-all">
        <!-- Mock Video Background -->
        <div class="absolute inset-0 bg-gradient-to-br from-[#121414] to-[#1e2020] opacity-80"></div>
        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=1200" alt="Video thumbnail" class="absolute inset-0 w-full h-full object-cover mix-blend-overlay opacity-30 group-hover:opacity-40 transition-opacity duration-500" />
        
        <!-- Play Button -->
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-16 h-16 bg-[#bef264] rounded-full flex items-center justify-center text-[#131f00] shadow-[0_0_30px_rgba(190,242,100,0.3)] group-hover:scale-110 transition-transform duration-300">
            <span class="material-symbols-outlined text-3xl ml-1">play_arrow</span>
          </div>
        </div>

        <!-- Video Details -->
        <div class="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/90 via-black/50 to-transparent">
          <p class="text-[10px] font-mono text-[#bef264] font-bold uppercase tracking-widest mb-1">Video Tutorial</p>
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-bold text-white">Mastering the PortalX Portal</h3>
            <span class="bg-black/60 px-2 py-1 rounded text-xs font-mono backdrop-blur-sm border border-white/10 text-white">12:45</span>
          </div>
        </div>
      </div>

      <!-- Progress Area -->
      <div class="lg:col-span-1 bg-[#171717] rounded-xl border border-white/5 p-8 flex flex-col items-center justify-center relative overflow-hidden">
        <h4 class="absolute top-6 left-6 text-xs font-mono uppercase tracking-widest text-gray-400 font-bold">Onboarding Progress</h4>
        
        <!-- Circular Progress (Mock) -->
        <div class="relative w-40 h-40 mt-8 mb-6">
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="6" />
            <circle cx="50" cy="50" r="45" fill="none" stroke="#bef264" stroke-width="6" stroke-dasharray="283" stroke-dashoffset="212" stroke-linecap="round" class="drop-shadow-[0_0_10px_rgba(190,242,100,0.5)]" />
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center text-white">
            <span class="text-4xl font-light tracking-tighter">25<span class="text-xl">%</span></span>
            <span class="text-[9px] font-mono uppercase tracking-widest text-gray-400 mt-1">Complete</span>
          </div>
        </div>

        <div class="w-full space-y-3 mt-4">
          <div class="flex justify-between items-center text-sm border-b border-white/5 pb-2">
            <span class="text-gray-400">Estimated Time</span>
            <span class="text-white font-medium">15 mins left</span>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-gray-400">Active Module</span>
            <span class="text-white font-medium">Infrastructure Sync</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Getting Started Steps -->
    <div class="pt-8">
      <h3 class="font-display text-2xl font-bold text-white mb-6">Getting Started</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- Step 1: Complete -->
        <div class="bg-[#1e2020] border border-white/5 p-6 rounded-xl relative opacity-60 flex flex-col justify-between group transition-all">
          <div class="absolute top-4 right-4 text-[#bef264]">
            <span class="material-symbols-outlined">check_circle</span>
          </div>
          <div>
            <div class="w-10 h-10 rounded bg-white/5 flex items-center justify-center text-gray-300 font-mono text-sm font-bold mb-4">01</div>
            <h4 class="font-bold text-white mb-2">Complete Profile</h4>
            <p class="text-xs text-gray-400 leading-relaxed h-20 line-clamp-4">Update your professional details and notification preferences for seamless communication.</p>
          </div>
          <button class="w-full py-2.5 mt-4 bg-white/5 hover:bg-white/10 text-gray-300 rounded-lg text-xs font-bold transition-all border border-white/5">
            Edit Profile
          </button>
        </div>

        <!-- Step 2: Active -->
        <div class="bg-[#171717] border border-[#bef264]/30 p-6 rounded-xl relative flex flex-col justify-between shadow-[0_0_20px_rgba(190,242,100,0.05)] transform -translate-y-1">
          <div class="absolute top-4 right-4">
            <div class="w-5 h-5 rounded-full border-2 border-gray-600"></div>
          </div>
          <div>
            <div class="w-10 h-10 rounded bg-[#bef264] flex items-center justify-center text-[#131f00] font-mono text-sm font-bold mb-4">02</div>
            <h4 class="font-bold text-white mb-2">Active Projects</h4>
            <p class="text-xs text-gray-400 leading-relaxed h-20 line-clamp-4">Review your initial scope of work and approve the project roadmap milestones.</p>
          </div>
          <button class="w-full py-2.5 mt-4 bg-[#bef264] hover:bg-[#a3d64c] text-[#131f00] rounded-lg text-xs font-bold transition-all">
            View Projects
          </button>
        </div>

        <!-- Step 3: Locked -->
        <div class="bg-[#121414] border border-white/5 p-6 rounded-xl relative opacity-40 flex flex-col justify-between group">
          <div class="absolute top-4 right-4 text-gray-600">
            <span class="material-symbols-outlined text-sm">lock</span>
          </div>
          <div>
            <div class="w-10 h-10 rounded bg-white/5 flex items-center justify-center text-gray-500 font-mono text-sm font-bold mb-4 border border-white/5">03</div>
            <h4 class="font-bold text-gray-400 mb-2">Billing Setup</h4>
            <p class="text-xs text-gray-500 leading-relaxed h-20 line-clamp-4">Securely link your payment method and configure automated invoicing.</p>
          </div>
          <button disabled class="w-full py-2.5 mt-4 bg-white/5 text-gray-500 rounded-lg text-xs font-bold border border-transparent cursor-not-allowed">
            Locked
          </button>
        </div>

        <!-- Step 4: Locked -->
        <div class="bg-[#121414] border border-white/5 p-6 rounded-xl relative opacity-40 flex flex-col justify-between group">
          <div class="absolute top-4 right-4 text-gray-600">
            <span class="material-symbols-outlined text-sm">lock</span>
          </div>
          <div>
            <div class="w-10 h-10 rounded bg-white/5 flex items-center justify-center text-gray-500 font-mono text-sm font-bold mb-4 border border-white/5">04</div>
            <h4 class="font-bold text-gray-400 mb-2">Message Manager</h4>
            <p class="text-xs text-gray-500 leading-relaxed h-20 line-clamp-4">Schedule your first sync call with your dedicated account success manager.</p>
          </div>
          <button disabled class="w-full py-2.5 mt-4 bg-white/5 text-gray-500 rounded-lg text-xs font-bold border border-transparent cursor-not-allowed">
            Locked
          </button>
        </div>

      </div>
    </div>

    <!-- Final CTA Area -->
    <div class="mt-8 bg-[#171717] border border-white/5 rounded-xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-full border border-[#bef264]/30 flex items-center justify-center text-[#bef264]">
          <span class="material-symbols-outlined">speed</span>
        </div>
        <div>
          <h4 class="font-bold text-white text-lg">Ready to accelerate?</h4>
          <p class="text-sm text-gray-400">Complete Step 2 to unlock the full potential of your dashboard.</p>
        </div>
      </div>
      <div class="flex items-center gap-3 w-full md:w-auto">
        <button class="flex-1 md:flex-none py-3 px-8 bg-[#bef264] hover:bg-[#a3d64c] text-[#131f00] rounded-lg font-bold transition-all whitespace-nowrap text-sm">
          Get Started
        </button>
          <button v-if="!isCompleted" @click="dismissOnboarding" class="flex-1 md:flex-none py-3 px-6 bg-[#1e2020] hover:bg-[#252828] text-white rounded-lg font-bold border border-white/5 transition-all whitespace-nowrap text-sm flex items-center justify-center gap-2">
            <span v-if="isDismissing" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
            Mark as Complete
          </button>
          <span v-else class="text-[#bef264] flex items-center gap-2 font-bold font-mono uppercase tracking-widest text-xs">
            <span class="material-symbols-outlined text-[18px]">check_circle</span>
            Completed
          </span>
        </div>
      </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '~/composables/useApi'

definePageMeta({
  layout: 'portal'
})

const route = useRoute()
const router = useRouter()
const api = useApi()

const me = ref(null)
const projects = ref([])
const isDismissing = ref(false)
const isLoading = ref(true)

const isCompleted = computed(() => !!me.value?.onboarding_dismissed_at)

onMounted(async () => {
  try {
    const [meData, projectsData] = await Promise.all([
      api('/api/v1/portal/me').catch(() => null),
      api('/api/v1/portal/projects').catch(() => [])
    ])
    me.value = meData
    projects.value = projectsData || []
  } catch (error) {
    console.error('Failed to load onboarding data', error)
  } finally {
    isLoading.value = false
  }
})

const dismissOnboarding = async () => {
  if (isDismissing.value) return
  isDismissing.value = true
  try {
    await api('/api/v1/portal/onboarding/dismiss', { method: 'POST' })
    if (me.value) {
      me.value.onboarding_dismissed_at = new Date().toISOString()
    }
    // Automatically route to dashboard
    router.push(`/portal/${route.params.token}`)
  } catch (error) {
    console.error('Failed to dismiss onboarding', error)
  } finally {
    isDismissing.value = false
  }
}
</script>
