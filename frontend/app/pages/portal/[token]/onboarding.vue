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
    <div :class="['grid gap-8 pt-4', isCompleted ? 'grid-cols-1 max-w-4xl mx-auto' : 'grid-cols-1 lg:grid-cols-3']">
      
      <!-- Video Area -->
      <div :class="['relative bg-[#171717] rounded-xl overflow-hidden border border-white/5 aspect-video group shadow-lg hover:border-[#bef264]/30 transition-all', isCompleted ? 'col-span-1' : 'lg:col-span-2']">
        <!-- Mock Video Background -->
        <div class="absolute inset-0 bg-gradient-to-br from-[#121414] to-[#1e2020] opacity-80"></div>
        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=1200" alt="Video thumbnail" class="absolute inset-0 w-full h-full object-cover mix-blend-overlay opacity-30 group-hover:opacity-40 transition-opacity duration-500" />
        
        <!-- Play Button -->
        <div class="absolute inset-0 flex items-center justify-center cursor-pointer">
          <div class="w-16 h-16 bg-[#bef264] rounded-full flex items-center justify-center text-[#131f00] shadow-[0_0_30px_rgba(190,242,100,0.3)] group-hover:scale-110 transition-transform duration-300">
            <span class="material-symbols-outlined text-3xl ml-1">play_arrow</span>
          </div>
        </div>

        <!-- Video Details -->
        <div class="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/90 via-black/50 to-transparent pointer-events-none">
          <p class="text-[10px] font-mono text-[#bef264] font-bold uppercase tracking-widest mb-1">Video Tutorial</p>
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-bold text-white">Mastering the Command Center</h3>
            <span class="bg-black/60 px-2 py-1 rounded text-xs font-mono backdrop-blur-sm border border-white/10 text-white">12:45</span>
          </div>
        </div>
      </div>

      <!-- Progress Area -->
      <div v-if="!isCompleted" class="lg:col-span-1 bg-[#171717] rounded-xl border border-white/5 p-8 flex flex-col items-center justify-center relative overflow-hidden">
        <h4 class="absolute top-6 left-6 text-xs font-mono uppercase tracking-widest text-gray-400 font-bold">Onboarding Progress</h4>
        
        <!-- Circular Progress -->
        <div class="relative w-40 h-40 mt-8 mb-6">
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="6" />
            <circle cx="50" cy="50" r="45" fill="none" stroke="#bef264" stroke-width="6" :stroke-dasharray="283" :stroke-dashoffset="283 - (283 * progressPercentage / 100)" stroke-linecap="round" class="drop-shadow-[0_0_10px_rgba(190,242,100,0.5)] transition-all duration-1000" />
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center text-white">
            <span class="text-4xl font-light tracking-tighter">{{ Math.round(progressPercentage) }}<span class="text-xl">%</span></span>
            <span class="text-[9px] font-mono uppercase tracking-widest text-gray-400 mt-1">Complete</span>
          </div>
        </div>

        <div class="w-full space-y-3 mt-4">
          <div class="flex justify-between items-center text-sm border-b border-white/5 pb-2">
            <span class="text-gray-400">Steps Completed</span>
            <span class="text-white font-medium">{{ completedSteps.length }} of 4</span>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-gray-400">Next Module</span>
            <span class="text-white font-medium">{{ nextStepName }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Getting Started Steps -->
    <div v-if="!isCompleted" class="pt-8">
      <h3 class="font-display text-2xl font-bold text-white mb-6">Getting Started</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- Step 1: Complete Profile -->
        <div :class="['border p-6 rounded-xl relative flex flex-col justify-between group transition-all', isStepDone(1) ? 'bg-[#1e2020] border-white/5 opacity-60' : (isStepActive(1) ? 'bg-[#171717] border-[#bef264]/30 shadow-[0_0_20px_rgba(190,242,100,0.05)] transform -translate-y-1' : 'bg-[#121414] border-white/5 opacity-40')]">
          <div v-if="isStepDone(1)" class="absolute top-4 right-4 text-[#bef264]">
            <span class="material-symbols-outlined">check_circle</span>
          </div>
          <div v-else-if="isStepActive(1)" class="absolute top-4 right-4">
            <div class="w-5 h-5 rounded-full border-2 border-gray-600"></div>
          </div>
          <div v-else class="absolute top-4 right-4 text-gray-600">
            <span class="material-symbols-outlined text-sm">lock</span>
          </div>
          
          <div>
            <div :class="['w-10 h-10 rounded flex items-center justify-center font-mono text-sm font-bold mb-4', isStepDone(1) ? 'bg-white/5 text-gray-300' : (isStepActive(1) ? 'bg-[#bef264] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-white/5')]">01</div>
            <h4 :class="['font-bold mb-2', isStepDone(1) || isStepActive(1) ? 'text-white' : 'text-gray-400']">Complete Profile</h4>
            <p :class="['text-xs leading-relaxed h-20 line-clamp-4', isStepDone(1) || isStepActive(1) ? 'text-gray-400' : 'text-gray-500']">Update your professional details and notification preferences for seamless communication.</p>
          </div>
          <button @click="goToStep(1, 'settings')" :disabled="!isStepActive(1) && !isStepDone(1)" :class="['w-full py-2.5 mt-4 rounded-lg text-xs font-bold transition-all', isStepDone(1) ? 'bg-white/5 hover:bg-white/10 text-gray-300 border border-white/5' : (isStepActive(1) ? 'bg-[#bef264] hover:bg-[#a3d64c] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-transparent cursor-not-allowed')]">
            {{ isStepDone(1) ? 'Review Profile' : (isStepActive(1) ? 'Edit Profile' : 'Locked') }}
          </button>
        </div>

        <!-- Step 2: Active Projects -->
        <div :class="['border p-6 rounded-xl relative flex flex-col justify-between group transition-all', isStepDone(2) ? 'bg-[#1e2020] border-white/5 opacity-60' : (isStepActive(2) ? 'bg-[#171717] border-[#bef264]/30 shadow-[0_0_20px_rgba(190,242,100,0.05)] transform -translate-y-1' : 'bg-[#121414] border-white/5 opacity-40')]">
          <div v-if="isStepDone(2)" class="absolute top-4 right-4 text-[#bef264]">
            <span class="material-symbols-outlined">check_circle</span>
          </div>
          <div v-else-if="isStepActive(2)" class="absolute top-4 right-4">
            <div class="w-5 h-5 rounded-full border-2 border-gray-600"></div>
          </div>
          <div v-else class="absolute top-4 right-4 text-gray-600">
            <span class="material-symbols-outlined text-sm">lock</span>
          </div>
          
          <div>
            <div :class="['w-10 h-10 rounded flex items-center justify-center font-mono text-sm font-bold mb-4', isStepDone(2) ? 'bg-white/5 text-gray-300' : (isStepActive(2) ? 'bg-[#bef264] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-white/5')]">02</div>
            <h4 :class="['font-bold mb-2', isStepDone(2) || isStepActive(2) ? 'text-white' : 'text-gray-400']">Active Projects</h4>
            <p :class="['text-xs leading-relaxed h-20 line-clamp-4', isStepDone(2) || isStepActive(2) ? 'text-gray-400' : 'text-gray-500']">Review your initial scope of work and approve the project roadmap milestones.</p>
          </div>
          <button @click="goToStep(2, '')" :disabled="!isStepActive(2) && !isStepDone(2)" :class="['w-full py-2.5 mt-4 rounded-lg text-xs font-bold transition-all', isStepDone(2) ? 'bg-white/5 hover:bg-white/10 text-gray-300 border border-white/5' : (isStepActive(2) ? 'bg-[#bef264] hover:bg-[#a3d64c] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-transparent cursor-not-allowed')]">
            {{ isStepDone(2) ? 'Review Projects' : (isStepActive(2) ? 'View Projects' : 'Locked') }}
          </button>
        </div>

        <!-- Step 3: Billing Setup -->
        <div :class="['border p-6 rounded-xl relative flex flex-col justify-between group transition-all', isStepDone(3) ? 'bg-[#1e2020] border-white/5 opacity-60' : (isStepActive(3) ? 'bg-[#171717] border-[#bef264]/30 shadow-[0_0_20px_rgba(190,242,100,0.05)] transform -translate-y-1' : 'bg-[#121414] border-white/5 opacity-40')]">
          <div v-if="isStepDone(3)" class="absolute top-4 right-4 text-[#bef264]">
            <span class="material-symbols-outlined">check_circle</span>
          </div>
          <div v-else-if="isStepActive(3)" class="absolute top-4 right-4">
            <div class="w-5 h-5 rounded-full border-2 border-gray-600"></div>
          </div>
          <div v-else class="absolute top-4 right-4 text-gray-600">
            <span class="material-symbols-outlined text-sm">lock</span>
          </div>

          <div>
            <div :class="['w-10 h-10 rounded flex items-center justify-center font-mono text-sm font-bold mb-4', isStepDone(3) ? 'bg-white/5 text-gray-300' : (isStepActive(3) ? 'bg-[#bef264] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-white/5')]">03</div>
            <h4 :class="['font-bold mb-2', isStepDone(3) || isStepActive(3) ? 'text-white' : 'text-gray-400']">Forms & Info</h4>
            <p :class="['text-xs leading-relaxed h-20 line-clamp-4', isStepDone(3) || isStepActive(3) ? 'text-gray-400' : 'text-gray-500']">Securely provide required onboarding info, documents, and submit active forms.</p>
          </div>
          <button @click="goToStep(3, 'forms')" :disabled="!isStepActive(3) && !isStepDone(3)" :class="['w-full py-2.5 mt-4 rounded-lg text-xs font-bold transition-all', isStepDone(3) ? 'bg-white/5 hover:bg-white/10 text-gray-300 border border-white/5' : (isStepActive(3) ? 'bg-[#bef264] hover:bg-[#a3d64c] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-transparent cursor-not-allowed')]">
            {{ isStepDone(3) ? 'Review Forms' : (isStepActive(3) ? 'View Forms' : 'Locked') }}
          </button>
        </div>

        <!-- Step 4: Message Manager -->
        <div :class="['border p-6 rounded-xl relative flex flex-col justify-between group transition-all', isStepDone(4) ? 'bg-[#1e2020] border-white/5 opacity-60' : (isStepActive(4) ? 'bg-[#171717] border-[#bef264]/30 shadow-[0_0_20px_rgba(190,242,100,0.05)] transform -translate-y-1' : 'bg-[#121414] border-white/5 opacity-40')]">
          <div v-if="isStepDone(4)" class="absolute top-4 right-4 text-[#bef264]">
            <span class="material-symbols-outlined">check_circle</span>
          </div>
          <div v-else-if="isStepActive(4)" class="absolute top-4 right-4">
            <div class="w-5 h-5 rounded-full border-2 border-gray-600"></div>
          </div>
          <div v-else class="absolute top-4 right-4 text-gray-600">
            <span class="material-symbols-outlined text-sm">lock</span>
          </div>

          <div>
            <div :class="['w-10 h-10 rounded flex items-center justify-center font-mono text-sm font-bold mb-4', isStepDone(4) ? 'bg-white/5 text-gray-300' : (isStepActive(4) ? 'bg-[#bef264] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-white/5')]">04</div>
            <h4 :class="['font-bold mb-2', isStepDone(4) || isStepActive(4) ? 'text-white' : 'text-gray-400']">Message Manager</h4>
            <p :class="['text-xs leading-relaxed h-20 line-clamp-4', isStepDone(4) || isStepActive(4) ? 'text-gray-400' : 'text-gray-500']">Say hello and schedule your first sync call with your dedicated account manager.</p>
          </div>
          <button @click="goToStep(4, 'messages')" :disabled="!isStepActive(4) && !isStepDone(4)" :class="['w-full py-2.5 mt-4 rounded-lg text-xs font-bold transition-all', isStepDone(4) ? 'bg-white/5 hover:bg-white/10 text-gray-300 border border-white/5' : (isStepActive(4) ? 'bg-[#bef264] hover:bg-[#a3d64c] text-[#131f00]' : 'bg-white/5 text-gray-500 border border-transparent cursor-not-allowed')]">
            {{ isStepDone(4) ? 'Review Messages' : (isStepActive(4) ? 'Open Messages' : 'Locked') }}
          </button>
        </div>

      </div>
    </div>

    <!-- Final CTA Area -->
    <div v-if="!isCompleted" class="mt-8 bg-[#171717] border border-white/5 rounded-xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-full border border-[#bef264]/30 flex items-center justify-center text-[#bef264]">
          <span class="material-symbols-outlined">speed</span>
        </div>
        <div>
          <h4 class="font-bold text-white text-lg">{{ progressPercentage === 100 ? 'You are all set!' : 'Ready to accelerate?' }}</h4>
          <p class="text-sm text-gray-400">{{ progressPercentage === 100 ? 'You have completed all steps. You can finalize your onboarding.' : `Complete Step ${completedSteps.length + 1} to unlock the full potential of your dashboard.` }}</p>
        </div>
      </div>
      <div class="flex items-center gap-3 w-full md:w-auto">
        <button v-if="progressPercentage < 100" @click="goToStep(completedSteps.length + 1, getRouteForStep(completedSteps.length + 1))" class="flex-1 md:flex-none py-3 px-8 bg-[#bef264] hover:bg-[#a3d64c] text-[#131f00] rounded-lg font-bold transition-all whitespace-nowrap text-sm">
          Continue Onboarding
        </button>
          <button @click="dismissOnboarding" class="flex-1 md:flex-none py-3 px-6 bg-[#1e2020] hover:bg-[#bef264] hover:text-[#131f00] text-white rounded-lg font-bold border border-white/5 transition-all whitespace-nowrap text-sm flex items-center justify-center gap-2">
            <span v-if="isDismissing" class="material-symbols-outlined animate-spin text-sm">progress_activity</span>
            {{ progressPercentage === 100 ? 'Finalize Onboarding' : 'Skip & Mark Complete' }}
          </button>
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

const completedSteps = ref([])

const isCompleted = computed(() => !!me.value?.onboarding_dismissed_at)

const progressPercentage = computed(() => {
  return (completedSteps.value.length / 4) * 100
})

const nextStepName = computed(() => {
  const steps = ["Complete Profile", "Active Projects", "Forms & Info", "Message Manager"]
  if (completedSteps.value.length >= 4) return "All Complete"
  return steps[completedSteps.value.length]
})

const isStepDone = (step) => completedSteps.value.includes(step)
const isStepActive = (step) => completedSteps.value.length + 1 >= step

const getRouteForStep = (step) => {
  const routes = {
    1: 'settings',
    2: '',
    3: 'forms',
    4: 'messages'
  }
  return routes[step]
}

const goToStep = (step, path) => {
  if (!isStepActive(step)) return
  
  // Mark this step as completed locally if not already
  if (!completedSteps.value.includes(step)) {
    completedSteps.value.push(step)
    if (me.value?.id) {
      localStorage.setItem(`onboarding_${me.value.id}`, JSON.stringify(completedSteps.value))
    }
  }

  // Navigate
  router.push(`/portal/${route.params.token}/${path}`)
}

onMounted(async () => {
  try {
    const [meData, projectsData] = await Promise.all([
      api('/api/v1/portal/me').catch(() => null),
      api('/api/v1/portal/projects').catch(() => [])
    ])
    me.value = meData
    projects.value = projectsData || []

    // Load progress from local storage
    if (meData?.id) {
      const saved = localStorage.getItem(`onboarding_${meData.id}`)
      if (saved) {
        completedSteps.value = JSON.parse(saved)
      } else {
        // Initialize step 1 as active, so completed steps is empty
        completedSteps.value = []
      }
    }
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
    // We don't route them away anymore, we let the UI reactively hide the sections
    // router.push(`/portal/${route.params.token}`)
  } catch (error) {
    console.error('Failed to dismiss onboarding', error)
  } finally {
    isDismissing.value = false
  }
}
</script>
