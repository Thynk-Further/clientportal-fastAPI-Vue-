<script setup>
useHead({
  link: [
    {
      rel: 'stylesheet',
      href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200'
    }
  ]
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<style>
/* Material Icons Outlined Integration support */

.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
}

body {
  background-color: #121414;
  color: #e3e2e2;
  -webkit-font-smoothing: antialiased;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #292a2a;
  border-radius: 9999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #343535;
}
</style>
