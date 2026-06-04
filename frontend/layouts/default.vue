<template>
  <div class="min-h-screen bg-gray-50 flex font-sans">
    <aside class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col">
      <div class="p-6">
        <h1 class="text-xl font-bold text-gray-900 tracking-tight">ClientPortal</h1>
      </div>
      <nav class="mt-2 px-4 space-y-1 flex-1">
        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4 px-2">Dashboard</p>
        <a href="#" class="block px-2 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-md">Overview</a>
        <a href="#" class="block px-2 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-md">Clients</a>
        <a href="#" class="block px-2 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-md">Projects</a>
      </nav>
      <div class="p-4 border-t border-gray-200">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
            F
          </div>
          <div>
            <p class="text-sm font-medium text-gray-900">Freelancer</p>
            <p class="text-xs text-gray-500">Free Plan</p>
          </div>
        </div>
      </div>
    </aside>

    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="bg-white border-b border-gray-200 h-16 flex items-center px-6 justify-between">
        <div class="md:hidden">
          <span class="font-bold text-gray-900">ClientPortal</span>
        </div>
        <div class="flex-1"></div>
        <div class="flex items-center gap-4">
          <button class="text-gray-500 hover:text-gray-700">
            <!-- Icon placeholder -->
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
          </button>
        </div>
      </header>
      <main class="flex-1 overflow-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
