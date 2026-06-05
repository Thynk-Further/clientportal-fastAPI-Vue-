<template>
  <div class="min-h-screen bg-[#121414] text-[#e3e2e2] flex flex-col font-sans antialiased text-sm">
    
    <!-- Portal Header (White-labeled) -->
    <header class="bg-[#121414] border-b border-white/5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          
          <!-- Branding Area (Will be dynamic later) -->
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-[#bef264] rounded-lg flex items-center justify-center text-[#131f00] font-bold shadow-md">
              <span class="material-symbols-outlined text-lg leading-none">account_tree</span>
            </div>
            <span class="font-display font-bold text-white text-xl tracking-tight">PortalX</span>
          </div>

          <!-- Client Info -->
          <div class="flex items-center gap-4">
            <span class="text-xs font-bold text-gray-400 font-mono tracking-wider uppercase flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-[#bef264] animate-pulse"></span>
              Secure Portal Session
            </span>
          </div>

        </div>
      </div>
    </header>

    <!-- Portal Main Content -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 relative z-10">
      <slot />
    </main>
    
    <!-- Portal Footer -->
    <footer class="bg-[#121414] border-t border-white/5 py-6 mt-10 relative z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-center items-center">
        <p class="text-xs text-gray-500 font-mono">Powered by PortalX Technologies</p>
      </div>
    </footer>

    <!-- Decorative background elements -->
    <div class="fixed top-[-10%] right-[-10%] w-[500px] h-[500px] pointer-events-none rounded-full bg-[radial-gradient(circle_at_center,rgba(190,242,100,0.08)_0%,transparent_70%)] z-0"></div>
    <div class="fixed bottom-[-10%] left-[-10%] w-[500px] h-[500px] pointer-events-none rounded-full bg-[radial-gradient(circle_at_center,rgba(190,242,100,0.08)_0%,transparent_70%)] z-0"></div>

  </div>
</template>
