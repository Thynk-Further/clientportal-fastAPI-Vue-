<template>
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans">
    
    <!-- Portal Header (White-labeled) -->
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          
          <!-- Branding Area (Will be dynamic later) -->
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold">
              CP
            </div>
            <span class="font-bold text-gray-900 text-lg tracking-tight">ClientPortal</span>
          </div>

          <!-- Client Info -->
          <div class="flex items-center gap-4">
            <span class="text-sm font-medium text-gray-500">Client Access</span>
          </div>

        </div>
      </div>
    </header>

    <!-- Portal Main Content -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <slot />
    </main>
    
    <!-- Portal Footer -->
    <footer class="bg-white border-t border-gray-200 py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-center items-center">
        <p class="text-xs text-gray-400">Powered by ClientPortal</p>
      </div>
    </footer>

  </div>
</template>
