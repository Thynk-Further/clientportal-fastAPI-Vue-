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

    <!-- Main Content -->
    <div class="space-y-10">
      
      <!-- Profile Section -->
      <section class="bg-[#171717] border border-white/5 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#1e2020]/50">
          <div>
            <h2 class="font-bold text-white text-lg">Personal Profile</h2>
            <p class="text-xs text-gray-400 mt-1">Update your personal information and contact details.</p>
          </div>
          <button class="bg-[#bef264] text-[#131f00] font-bold text-xs px-4 py-2 rounded-lg hover:bg-[#a3d64c] transition-colors">
            Save Changes
          </button>
        </div>
        
        <div class="p-6 space-y-6">
          <div class="flex items-center gap-6">
            <div class="w-20 h-20 rounded-full border border-white/10 bg-[#1e2020] overflow-hidden shrink-0">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="Avatar" class="w-full h-full object-cover opacity-80" />
            </div>
            <div>
              <button class="bg-white/5 hover:bg-white/10 text-white border border-white/10 px-4 py-2 rounded-lg text-xs font-bold transition-colors mb-2">
                Change Avatar
              </button>
              <p class="text-[10px] text-gray-500 font-mono uppercase">JPG, GIF or PNG. Max 1MB.</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-xs text-gray-400 font-mono uppercase tracking-widest block">Full Name</label>
              <input type="text" value="Alex Sterling" class="w-full bg-[#1e2020] border border-white/5 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-[#bef264]/50 transition-colors" />
            </div>
            <div class="space-y-2">
              <label class="text-xs text-gray-400 font-mono uppercase tracking-widest block">Job Title</label>
              <input type="text" value="Chief Marketing Officer" class="w-full bg-[#1e2020] border border-white/5 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-[#bef264]/50 transition-colors" />
            </div>
            <div class="space-y-2 md:col-span-2">
              <label class="text-xs text-gray-400 font-mono uppercase tracking-widest block">Email Address</label>
              <input type="email" value="alex@company.com" disabled class="w-full bg-[#1e2020]/50 border border-white/5 rounded-lg p-3 text-sm text-gray-500 cursor-not-allowed" />
              <p class="text-[10px] text-gray-500 mt-1">To change your email address, please contact support.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Team Members Section -->
      <section class="bg-[#171717] border border-white/5 rounded-xl overflow-hidden">
        <div class="px-6 py-5 border-b border-white/5 flex justify-between items-center bg-[#1e2020]/50">
          <div>
            <h2 class="font-bold text-white text-lg">Team Access</h2>
            <p class="text-xs text-gray-400 mt-1">Invite up to 3 team members to collaborate in this portal.</p>
          </div>
          <button class="bg-white/5 hover:bg-white/10 text-white border border-white/10 font-bold text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-2">
            <span class="material-symbols-outlined text-[16px]">add</span>
            Invite Member
          </button>
        </div>
        
        <div class="divide-y divide-white/5">
          <div class="px-6 py-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-[#1e2020] border border-white/10 flex items-center justify-center text-white font-bold text-sm">
                AS
              </div>
              <div>
                <h4 class="text-sm font-bold text-white">Alex Sterling <span class="bg-[#bef264]/10 text-[#bef264] px-2 py-0.5 rounded text-[9px] font-mono ml-2 uppercase">Primary</span></h4>
                <p class="text-xs text-gray-500">alex@company.com</p>
              </div>
            </div>
          </div>

          <div class="px-6 py-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-[#1e2020] border border-white/10 flex items-center justify-center text-gray-400 font-bold text-sm">
                JD
              </div>
              <div>
                <h4 class="text-sm font-bold text-white">Jane Doe</h4>
                <p class="text-xs text-gray-500">jane.doe@company.com</p>
              </div>
            </div>
            <button class="text-gray-500 hover:text-red-400 transition-colors">
              <span class="material-symbols-outlined text-[18px]">delete</span>
            </button>
          </div>
        </div>
      </section>

      <!-- Danger Zone -->
      <section class="border border-red-500/20 rounded-xl overflow-hidden">
        <div class="p-6 flex items-center justify-between bg-red-500/5">
          <div>
            <h2 class="font-bold text-red-400 text-lg">Danger Zone</h2>
            <p class="text-xs text-red-400/70 mt-1">Permanently revoke all access tokens and sign out of all devices.</p>
          </div>
          <button class="bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 text-red-400 font-bold text-xs px-4 py-2 rounded-lg transition-colors">
            Revoke Access
          </button>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'portal'
})
</script>
