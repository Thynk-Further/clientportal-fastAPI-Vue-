<template>
  <div class="h-[calc(100vh-180px)] md:h-[calc(100vh-140px)] flex flex-col md:flex-row gap-6 font-sans text-[#e3e2e2] max-w-7xl mx-auto w-full">
    
    <!-- Left Column: Recent Chats -->
    <div class="w-full md:w-80 flex-shrink-0 flex flex-col bg-[#171717] rounded-xl border border-white/5 overflow-hidden">
      <div class="p-4 border-b border-white/5">
        <h2 class="font-display font-bold text-white text-lg">Recent Chats</h2>
      </div>
      
      <div class="flex-1 overflow-y-auto custom-scrollbar">
        <!-- Active Chat -->
        <div class="p-4 border-b border-white/5 bg-white/[0.02] border-l-2 border-l-[#bef264] cursor-pointer hover:bg-white/[0.04] transition-colors relative">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-[#1e2020] border border-white/10 flex items-center justify-center text-[#bef264]">
              <span class="material-symbols-outlined text-xl">architecture</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-baseline mb-0.5">
                <h4 class="font-bold text-white text-sm truncate">Neo-Metropolis Hub</h4>
                <span class="text-[9px] font-mono text-gray-500 shrink-0">12:45 PM</span>
              </div>
              <p class="text-xs text-[#bef264] truncate">Alex: Final render uploaded for ...</p>
            </div>
          </div>
        </div>

        <!-- Inactive Chat 1 -->
        <div class="p-4 border-b border-white/5 border-l-2 border-l-transparent cursor-pointer hover:bg-white/[0.02] transition-colors opacity-70 hover:opacity-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-[#1e2020] border border-white/10 flex items-center justify-center text-gray-400">
              <span class="material-symbols-outlined text-xl">layers</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-baseline mb-0.5">
                <h4 class="font-bold text-white text-sm truncate">Ethereal Branding</h4>
                <span class="text-[9px] font-mono text-gray-500 shrink-0">Yesterday</span>
              </div>
              <p class="text-xs text-gray-400 truncate">Sarah: The typography choice l...</p>
            </div>
          </div>
        </div>

        <!-- Inactive Chat 2 -->
        <div class="p-4 border-b border-white/5 border-l-2 border-l-transparent cursor-pointer hover:bg-white/[0.02] transition-colors opacity-70 hover:opacity-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-[#1e2020] border border-white/10 flex items-center justify-center text-gray-400">
              <span class="material-symbols-outlined text-xl">person</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-baseline mb-0.5">
                <h4 class="font-bold text-white text-sm truncate">Marcus (Manager)</h4>
                <span class="text-[9px] font-mono text-gray-500 shrink-0">Tue</span>
              </div>
              <p class="text-xs text-gray-400 truncate">Let's hop on a quick call to sync.</p>
            </div>
          </div>
        </div>

        <!-- Inactive Chat 3 -->
        <div class="p-4 border-b border-white/5 border-l-2 border-l-transparent cursor-pointer hover:bg-white/[0.02] transition-colors opacity-70 hover:opacity-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-[#1e2020] border border-white/10 flex items-center justify-center text-gray-400">
              <span class="material-symbols-outlined text-xl">payments</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-baseline mb-0.5">
                <h4 class="font-bold text-white text-sm truncate">Billing Support</h4>
                <span class="text-[9px] font-mono text-gray-500 shrink-0">Oct 12</span>
              </div>
              <p class="text-xs text-gray-400 truncate">Your invoice for Q3 is now avail...</p>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Right Column: Chat Interface -->
    <div class="flex-1 flex flex-col bg-[#121414] rounded-xl border border-white/5 overflow-hidden relative">
      
      <!-- Chat Header -->
      <div class="h-16 border-b border-white/5 flex items-center justify-between px-6 bg-[#171717] shrink-0">
        <div>
          <h2 class="font-display font-bold text-white text-lg flex items-center gap-2">
            Neo-Metropolis Hub
          </h2>
          <div class="flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-widest text-[#bef264] mt-0.5">
            <span class="w-1.5 h-1.5 bg-[#bef264] rounded-full"></span>
            Team Active
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button class="w-9 h-9 rounded bg-[#1e2020] border border-white/5 hover:bg-white/10 text-gray-300 flex items-center justify-center transition-colors">
            <span class="material-symbols-outlined text-[18px]">call</span>
          </button>
          <button class="w-9 h-9 rounded bg-[#1e2020] border border-white/5 hover:bg-white/10 text-gray-300 flex items-center justify-center transition-colors">
            <span class="material-symbols-outlined text-[18px]">videocam</span>
          </button>
          <button class="w-9 h-9 rounded bg-transparent hover:bg-white/5 text-gray-400 flex items-center justify-center transition-colors">
            <span class="material-symbols-outlined text-[18px]">more_vert</span>
          </button>
        </div>
      </div>

      <!-- Chat Messages Area -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar bg-[radial-gradient(ellipse_at_top_right,rgba(190,242,100,0.02),transparent_50%)]">
        
        <div class="flex justify-center">
          <span class="bg-[#1e2020] text-gray-500 text-[9px] font-mono uppercase tracking-widest px-3 py-1 rounded-full border border-white/5">
            October 24, 2023
          </span>
        </div>

        <!-- Incoming Message -->
        <div class="flex gap-4">
          <div class="w-8 h-8 rounded bg-[#bef264] flex items-center justify-center text-[#131f00] font-bold shrink-0 mt-6 border border-[#bef264]/20 shadow-[0_0_10px_rgba(190,242,100,0.2)]">
            <span class="material-symbols-outlined text-[16px]">bolt</span>
          </div>
          <div class="flex flex-col gap-1 max-w-[80%]">
            <span class="text-[10px] font-mono text-gray-500 ml-1">Obsidian Flux Team (Alex)</span>
            <div class="bg-[#1e2020] text-white p-4 rounded-2xl rounded-tl-sm border border-white/5 text-sm leading-relaxed shadow-sm">
              Hello! We've completed the preliminary structural phase of the Neo-Metropolis Hub project. Would you like to review the lighting studies today?
            </div>
            <span class="text-[9px] text-gray-500 ml-2">10:15 AM</span>
          </div>
        </div>

        <!-- Outgoing Message -->
        <div class="flex gap-4 flex-row-reverse">
          <div class="w-8 h-8 rounded-full overflow-hidden shrink-0 mt-6 border border-white/10">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="You" class="w-full h-full object-cover bg-gray-600" />
          </div>
          <div class="flex flex-col items-end gap-1 max-w-[80%]">
            <span class="text-[10px] font-mono text-gray-500 mr-1">You</span>
            <div class="bg-[#bef264] text-[#131f00] p-4 rounded-2xl rounded-tr-sm text-sm leading-relaxed font-medium shadow-sm">
              That sounds perfect. Can you also send over the latest wireframes for the lobby entrance?
            </div>
            <span class="text-[9px] text-gray-500 mr-2">10:20 AM</span>
          </div>
        </div>

        <!-- Incoming Message with Attachment -->
        <div class="flex gap-4">
          <div class="w-8 h-8 rounded bg-[#bef264] flex items-center justify-center text-[#131f00] font-bold shrink-0 mt-6 border border-[#bef264]/20 shadow-[0_0_10px_rgba(190,242,100,0.2)]">
            <span class="material-symbols-outlined text-[16px]">bolt</span>
          </div>
          <div class="flex flex-col gap-1 max-w-[80%]">
            <span class="text-[10px] font-mono text-gray-500 ml-1">Obsidian Flux Team (Alex)</span>
            <div class="bg-[#1e2020] text-white p-4 rounded-2xl rounded-tl-sm border border-white/5 text-sm leading-relaxed shadow-sm">
              Of course. Here is the draft PDF and a high-res rendering of the south-facing view.
              
              <div class="mt-4 flex flex-wrap gap-3">
                <!-- File Attachment -->
                <div class="flex items-center gap-3 bg-[#252828] p-3 rounded-xl border border-white/5 pr-4 cursor-pointer hover:bg-[#2c2f2f] transition-colors max-w-sm">
                  <div class="w-10 h-10 rounded bg-red-500/10 text-red-400 flex items-center justify-center shrink-0">
                    <span class="material-symbols-outlined">picture_as_pdf</span>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-white truncate">lobby_entrance_v2...</p>
                    <p class="text-[10px] text-gray-400 uppercase font-mono">2.4 MB</p>
                  </div>
                  <span class="material-symbols-outlined text-gray-400">download</span>
                </div>
                
                <!-- Image Attachment -->
                <div class="w-48 h-32 rounded-xl overflow-hidden border border-white/5 relative group cursor-pointer">
                  <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=600" alt="Render" class="w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                    <span class="material-symbols-outlined text-white">zoom_in</span>
                  </div>
                </div>
              </div>
            </div>
            <span class="text-[9px] text-gray-500 ml-2">12:45 PM</span>
          </div>
        </div>

      </div>

      <!-- Chat Input Area -->
      <div class="p-4 bg-[#171717] border-t border-white/5 shrink-0">
        <div class="bg-[#1e2020] border border-white/10 rounded-xl p-2 flex items-end gap-2 focus-within:border-[#bef264]/50 transition-colors shadow-sm">
          <div class="flex gap-1 pb-1 px-1">
            <button class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white rounded-full hover:bg-white/5 transition-colors">
              <span class="material-symbols-outlined text-[20px]">add_circle</span>
            </button>
            <button class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white rounded-full hover:bg-white/5 transition-colors">
              <span class="material-symbols-outlined text-[20px]">attach_file</span>
            </button>
          </div>
          
          <textarea 
            rows="1" 
            placeholder="Type your message to the team..." 
            class="flex-1 bg-transparent border-none text-sm text-white resize-none outline-none py-2.5 max-h-32 custom-scrollbar placeholder-gray-500"
          ></textarea>
          
          <button class="w-10 h-10 rounded-lg bg-[#bef264] text-[#131f00] flex items-center justify-center hover:bg-[#a3d64c] transition-colors shadow-sm shrink-0 mb-0.5 mr-0.5">
            <span class="material-symbols-outlined text-[18px]">send</span>
          </button>
        </div>
        <div class="flex justify-between items-center mt-2 px-2">
          <span class="text-[9px] font-mono text-gray-600 uppercase tracking-widest">Shift + Enter for new line</span>
          <span class="text-[9px] font-mono text-gray-600 flex items-center gap-1"><span class="material-symbols-outlined text-[12px]">schedule</span> Replies within 2 hours</span>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
definePageMeta({
  layout: 'portal'
})
</script>
