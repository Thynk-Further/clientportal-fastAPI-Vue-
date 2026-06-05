<template>
  <div class="space-y-8 font-sans max-w-7xl mx-auto text-[#e3e2e2]">
    
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/5 pb-6">
      <div>
        <h1 class="font-display text-3xl font-bold tracking-tight text-white mb-2">
          My Projects
        </h1>
        <p class="text-sm text-gray-400 max-w-xl">
          Manage and monitor your ongoing initiatives at Obsidian Flux.
        </p>
      </div>
      <div class="flex items-center gap-3">
        <div class="bg-[#171717] rounded-lg border border-white/5 p-1 flex font-mono text-xs font-bold uppercase tracking-wider text-gray-400">
          <button class="px-4 py-1.5 rounded bg-white/10 text-white shadow-sm">All</button>
          <button class="px-4 py-1.5 rounded hover:bg-white/5 hover:text-white transition-colors">Active</button>
          <button class="px-4 py-1.5 rounded hover:bg-white/5 hover:text-white transition-colors">On Hold</button>
          <button class="px-4 py-1.5 rounded hover:bg-white/5 hover:text-white transition-colors">Archive</button>
        </div>
        <button class="bg-[#171717] border border-white/5 px-4 py-2 rounded-lg text-xs font-bold text-gray-300 flex items-center gap-2 hover:bg-[#1e2020] transition-colors h-[34px]">
          <span class="material-symbols-outlined text-[16px]">filter_list</span> Filters
        </button>
      </div>
    </div>

    <!-- Main Projects Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      
      <!-- Highlighted Project (Col Span 2) -->
      <div class="lg:col-span-2 bg-gradient-to-br from-[#171717] to-[#1e2020] border border-white/[0.08] p-6 md:p-8 rounded-xl flex flex-col justify-between hover:border-[#bef264]/30 transition-all group relative overflow-hidden">
        <div class="absolute top-0 right-0 w-64 h-64 bg-[#bef264]/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3 pointer-events-none"></div>
        
        <div class="space-y-4">
          <div class="flex justify-between items-start">
            <h3 class="font-bold text-[#bef264] text-lg">Project Obsidian: Core Integration</h3>
            <span class="bg-[#bef264]/10 text-[#bef264] text-[10px] font-mono font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-[#bef264]/20 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-[#bef264] animate-pulse"></span> IN PROGRESS
            </span>
          </div>
          <p class="text-sm text-gray-300 leading-relaxed max-w-lg">
            Full-scale digital transformation including legacy migration and modern UI/UX implementation for the main customer dashboard.
          </p>
        </div>

        <div class="mt-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
          <div class="flex items-center gap-8">
            <div>
              <p class="text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-1">Overall Progress</p>
              <div class="flex items-center gap-3">
                <span class="text-4xl font-light text-white tracking-tighter">74<span class="text-2xl text-gray-500">%</span></span>
                <div class="w-24 h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div class="w-[74%] h-full bg-[#bef264] rounded-full"></div>
                </div>
              </div>
            </div>
            <div class="hidden md:block w-px h-12 bg-white/10"></div>
            <div class="hidden md:block">
              <p class="text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-1">Next Milestone</p>
              <p class="font-bold text-white text-sm">API Handshake V2</p>
              <p class="text-xs text-gray-400 mt-0.5 flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">event</span> Due Oct 24, 2024</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="bg-[#bef264] text-[#131f00] hover:bg-[#a3d64c] px-6 py-2.5 rounded-lg font-bold transition-all text-sm shadow-sm">View Details</button>
            <button class="w-10 h-10 flex items-center justify-center bg-[#1e2020] border border-white/5 hover:bg-white/5 rounded-lg text-gray-300 transition-colors">
              <span class="material-symbols-outlined text-[18px]">download</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Secondary Project 1 -->
      <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col justify-between hover:bg-[#1a1c1c] transition-all group">
        <div class="space-y-4">
          <div class="flex justify-between items-start">
            <span class="bg-white/5 text-gray-400 text-[10px] font-mono font-bold uppercase tracking-widest px-2.5 py-1 rounded-md border border-white/10">ON HOLD</span>
            <span class="text-[10px] text-gray-500 font-mono">Due Nov 12</span>
          </div>
          <div>
            <h4 class="font-bold text-white text-md mb-2">Brand Identity Refresh</h4>
            <p class="text-xs text-gray-400 leading-relaxed line-clamp-3">Phase 2 visual exploration and style guide documentation for global markets.</p>
          </div>
        </div>
        
        <div class="mt-8 space-y-4">
          <div>
            <div class="flex justify-between text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-2">
              <span>45% Complete</span>
            </div>
            <div class="w-full h-1 bg-white/5 rounded-full overflow-hidden">
              <div class="w-[45%] h-full bg-gray-500 rounded-full"></div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button class="flex-1 bg-[#1e2020] hover:bg-[#252828] text-white border border-white/5 py-2 rounded-lg text-xs font-bold transition-all">Details</button>
            <button class="w-8 h-8 flex items-center justify-center bg-[#1e2020] border border-white/5 hover:bg-white/5 rounded-lg text-gray-400 transition-colors">
              <span class="material-symbols-outlined text-[16px]">download</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Secondary Project 2 -->
      <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col justify-between hover:bg-[#1a1c1c] transition-all group">
        <div class="space-y-4">
          <div class="flex justify-between items-start">
            <span class="bg-green-500/10 text-green-400 text-[10px] font-mono font-bold uppercase tracking-widest px-2.5 py-1 rounded-md border border-green-500/20">COMPLETED</span>
            <span class="text-[10px] text-gray-500 font-mono">Ended Sep 15</span>
          </div>
          <div>
            <h4 class="font-bold text-white text-md mb-2">Alpha Q3 SEO Strategy</h4>
            <p class="text-xs text-gray-400 leading-relaxed line-clamp-3">Comprehensive market analysis and keyword optimization plan for the new product launch.</p>
          </div>
        </div>
        
        <div class="mt-8 space-y-4">
          <div>
            <div class="flex justify-between text-[10px] font-mono text-green-400 uppercase tracking-widest mb-2">
              <span>100% Complete</span>
              <span class="material-symbols-outlined text-[14px]">check_circle</span>
            </div>
            <div class="w-full h-1 bg-white/5 rounded-full overflow-hidden">
              <div class="w-full h-full bg-green-500 rounded-full"></div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button class="flex-1 bg-[#1e2020] hover:bg-[#252828] text-white border border-white/5 py-2 rounded-lg text-xs font-bold transition-all">Review</button>
            <button class="w-8 h-8 flex items-center justify-center bg-[#1e2020] border border-green-500/20 hover:bg-green-500/10 rounded-lg text-green-400 transition-colors">
              <span class="material-symbols-outlined text-[16px]">download</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Secondary Project 3 -->
      <div class="bg-[#171717] border border-white/[0.08] p-6 rounded-xl flex flex-col justify-between hover:bg-[#1a1c1c] transition-all group relative overflow-hidden">
        <div class="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-[#bef264]/5 to-transparent pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <div class="space-y-4">
          <div class="flex justify-between items-start">
            <span class="bg-[#bef264]/10 text-[#bef264] text-[10px] font-mono font-bold uppercase tracking-widest px-2.5 py-1 rounded-md border border-[#bef264]/20">IN PROGRESS</span>
            <span class="text-[10px] text-gray-500 font-mono flex items-center gap-1">Due Dec 01</span>
          </div>
          <div>
            <h4 class="font-bold text-white text-md mb-2">Flux Mobile App MVP</h4>
            <p class="text-xs text-gray-400 leading-relaxed line-clamp-3">Initial development of the React Native client application with core flux capabilities.</p>
          </div>
        </div>
        
        <div class="mt-8 space-y-4 relative z-10">
          <div>
            <div class="flex justify-between items-end text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-2">
              <span>28% Complete</span>
              <span class="flex items-center gap-1 normal-case tracking-normal"><span class="material-symbols-outlined text-[14px]">calendar_today</span> Dec 1st</span>
            </div>
            <div class="w-full h-1 bg-white/5 rounded-full overflow-hidden">
              <div class="w-[28%] h-full bg-[#bef264] rounded-full"></div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button class="flex-1 bg-[#1e2020] hover:bg-[#252828] text-white border border-white/5 py-2 rounded-lg text-xs font-bold transition-all">Details</button>
            <button class="w-8 h-8 flex items-center justify-center bg-[#1e2020] border border-white/5 hover:bg-white/5 rounded-lg text-gray-400 transition-colors">
              <span class="material-symbols-outlined text-[16px]">download</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Add New / Initiate Flow Card -->
      <div class="bg-transparent border border-dashed border-white/10 p-6 rounded-xl flex flex-col items-center justify-center text-center hover:bg-white/[0.02] hover:border-[#bef264]/30 transition-all cursor-pointer group min-h-[250px]">
        <div class="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center text-gray-400 group-hover:text-[#bef264] group-hover:bg-[#bef264]/10 transition-colors mb-4 border border-white/5">
          <span class="material-symbols-outlined text-2xl">add</span>
        </div>
        <h4 class="font-bold text-white mb-1">Initiate New Flow</h4>
        <p class="text-xs text-gray-500 max-w-[200px]">Ready to scale? Click to request a new project quote.</p>
      </div>

    </div>

    <!-- Bottom Report CTA -->
    <div class="mt-4 bg-[#171717] border border-white/5 rounded-xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6 hover:border-[#bef264]/20 transition-colors cursor-pointer group">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-[#bef264] border border-white/5">
          <span class="material-symbols-outlined">monitoring</span>
        </div>
        <div>
          <h4 class="font-bold text-white text-base">Quarterly Velocity Report</h4>
          <p class="text-xs text-gray-400 mt-1 max-w-md line-clamp-2">Download your aggregated project performance and delivery metrics for Q3.</p>
        </div>
      </div>
      <button class="w-full md:w-auto py-3 px-6 bg-white/5 hover:bg-white/10 text-white rounded-lg font-bold border border-white/10 transition-all whitespace-nowrap text-sm flex items-center justify-center gap-2">
        <span class="material-symbols-outlined text-[18px]">description</span>
        Download Master Report (PDF)
      </button>
    </div>

  </div>
</template>

<script setup>
definePageMeta({
  layout: 'portal'
})
</script>
