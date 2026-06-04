<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded bg-indigo-600 shadow-sm flex items-center justify-center text-white font-bold">
            <!-- Logo placeholder -->
            B
          </div>
          <span class="font-semibold text-gray-900 tracking-tight">Brand Name</span>
        </div>
        <nav class="flex items-center gap-6 text-sm font-medium text-gray-600">
          <a href="#" class="text-indigo-600 transition-colors">Deliverables</a>
          <a href="#" class="hover:text-gray-900 transition-colors">Forms</a>
          <a href="#" class="hover:text-gray-900 transition-colors">Invoices</a>
        </nav>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <slot />
    </main>
    <footer class="mt-auto py-6 text-center text-sm text-gray-400">
      <p>Powered by ClientPortal</p>
    </footer>
  </div>
</template>
