<template>
  <div class="bg-[#121414] text-[#e3e2e2] min-h-screen flex font-sans antialiased text-sm">
    <!-- PERSISTENT LEFT SIDEBAR PANEL (Desktop-Only) -->
    <aside class="w-64 border-r border-white/5 bg-[#171717] flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none hidden md:flex z-10">
      <div class="flex flex-col gap-8 py-6">
        <!-- Logo container -->
        <div class="px-6 flex flex-col gap-1 font-display tracking-tight text-white">
          <span class="text-[10px] font-mono text-gray-500 uppercase tracking-widest font-bold">Client Portal</span>
          <div class="flex items-center gap-2 text-xl font-black">
            <span class="w-6 h-6 bg-[#bef264] rounded flex items-center justify-center text-[#131f00] shadow-sm">
              <span class="material-symbols-outlined text-sm leading-none">token</span>
            </span>
            PortalX
          </div>
        </div>

        <!-- Tab Navigation items -->
        <nav class="px-3 space-y-1.5 flex flex-col font-sans text-sm">
          
          <NuxtLink
            :to="`/portal/${route.params.token}`"
            class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-semibold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.02]"
            active-class="bg-[#1e2020] !text-white hover:!text-white border border-white/5 shadow-sm"
            exact-active-class="bg-[#1e2020] !text-white hover:!text-white border border-white/5 shadow-sm"
          >
            <span class="material-symbols-outlined text-md leading-none">dashboard</span>
            Dashboard
          </NuxtLink>

          <NuxtLink
            :to="`/portal/${route.params.token}/onboarding`"
            class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-semibold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.02]"
            active-class="bg-[#1e2020] !text-white hover:!text-white border border-white/5 shadow-sm"
          >
            <span class="material-symbols-outlined text-md leading-none">flag</span>
            Onboarding
          </NuxtLink>

          <NuxtLink
            :to="`/portal/${route.params.token}/projects`"
            class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-semibold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.02]"
            active-class="bg-[#1e2020] !text-white hover:!text-white border border-white/5 shadow-sm"
          >
            <span class="material-symbols-outlined text-md leading-none">folder_open</span>
            Projects
          </NuxtLink>

          <NuxtLink
            :to="`/portal/${route.params.token}/messages`"
            class="flex items-center justify-between px-4 py-2.5 rounded-lg font-semibold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.02]"
            active-class="bg-[#1e2020] !text-white hover:!text-white border border-white/5 shadow-sm"
          >
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined text-md leading-none">chat_bubble</span>
              Messages
            </div>
            <!-- Notification dot placeholder -->
            <!-- <span class="h-2 w-2 rounded-full bg-[#bef264]"></span> -->
          </NuxtLink>

          <NuxtLink
            :to="`/portal/${route.params.token}/settings`"
            class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-semibold transition-all cursor-pointer border-none text-left text-gray-400 hover:text-white hover:bg-white/[0.02]"
            active-class="bg-[#1e2020] !text-white hover:!text-white border border-white/5 shadow-sm"
          >
            <span class="material-symbols-outlined text-md leading-none">person</span>
            Account
          </NuxtLink>
        </nav>
      </div>

      <!-- Bottom block -->
      <div class="p-4 border-t border-white/5 font-sans bg-[#171717]">
        <button class="w-full py-2.5 bg-[#1e2020] hover:bg-[#252828] text-gray-300 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-2 cursor-pointer border border-white/5">
          Contact Support
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT LOADING GRID FRAME -->
    <div class="flex-grow flex flex-col min-w-0 max-h-screen overflow-y-auto bg-[#121414] relative">
      
      <!-- Top nav row (Desktop + Mobile) -->
      <header class="flex justify-between items-center px-6 md:px-10 h-16 border-b border-white/5 z-40 sticky top-0 bg-[#121414]/90 backdrop-blur">
        <!-- Breadcrumb / Header title -->
        <div class="flex items-center gap-6 text-sm font-semibold">
          <NuxtLink :to="`/portal/${route.params.token}`" class="text-white hover:text-[#bef264] transition-colors" exact-active-class="text-[#bef264] border-b-2 border-[#bef264] pb-5 translate-y-2.5">Dashboard</NuxtLink>
          <NuxtLink :to="`/portal/${route.params.token}/onboarding`" class="text-gray-400 hover:text-white transition-colors" active-class="text-[#bef264] border-b-2 border-[#bef264] pb-5 translate-y-2.5">Onboarding</NuxtLink>
          <NuxtLink :to="`/portal/${route.params.token}/projects`" class="text-gray-400 hover:text-white transition-colors" active-class="text-[#bef264] border-b-2 border-[#bef264] pb-5 translate-y-2.5">Resources</NuxtLink>
        </div>

        <!-- Right Side: Search & Profile -->
        <div class="flex items-center gap-4">
          <!-- Search placeholder -->
          <div class="hidden md:flex items-center bg-[#171717] border border-white/5 rounded-lg px-3 py-1.5 w-64 focus-within:border-[#bef264]/50 transition-colors">
            <span class="material-symbols-outlined text-gray-500 text-[18px]">search</span>
            <input type="text" placeholder="Search workflow..." class="bg-transparent border-none text-xs text-white outline-none w-full ml-2 placeholder-gray-500" />
          </div>

          <button class="text-gray-400 hover:text-white relative">
            <span class="material-symbols-outlined text-[20px]">notifications</span>
            <span class="absolute top-0 right-0 w-1.5 h-1.5 bg-[#bef264] rounded-full"></span>
          </button>
          
          <button class="text-gray-400 hover:text-white">
            <span class="material-symbols-outlined text-[20px]">settings</span>
          </button>

          <div class="h-8 w-8 rounded-full bg-gray-600 ml-2 overflow-hidden border border-white/10">
            <!-- Avatar Placeholder -->
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="Avatar" class="w-full h-full object-cover opacity-80" />
          </div>
        </div>
      </header>

      <!-- Dynamic active views dispatcher -->
      <main class="flex-grow p-6 md:p-8 lg:p-10 pb-24 md:pb-12 relative z-10">
        <slot />
      </main>

      <!-- Decorative background elements -->
      <div class="fixed bottom-0 right-0 w-[500px] h-[500px] pointer-events-none rounded-full bg-[radial-gradient(circle_at_center,rgba(190,242,100,0.03)_0%,transparent_70%)] z-0"></div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>
