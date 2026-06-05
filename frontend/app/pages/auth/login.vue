<template>
  <div class="bg-surface-container-lowest text-on-surface min-h-screen flex flex-col relative overflow-hidden">
    <!-- Decorative premium glows -->
    <div class="fixed inset-0 pointer-events-none opacity-[0.03] bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.15)_0%,transparent_100%)]"></div>
    <div class="fixed top-[-10%] right-[-10%] w-[500px] h-[500px] pointer-events-none rounded-full bg-[radial-gradient(circle_at_center,rgba(190,242,100,0.08)_0%,transparent_70%)]"></div>
    <div class="fixed bottom-[-10%] left-[-10%] w-[500px] h-[500px] pointer-events-none rounded-full bg-[radial-gradient(circle_at_center,rgba(190,242,100,0.08)_0%,transparent_70%)]"></div>

    <header class="fixed top-0 w-full z-50 flex justify-between items-center px-6 h-16 bg-[#121414] border-b border-white/[0.05]">
      <div class="font-display font-bold text-xl text-primary flex items-center gap-2">
        <span class="material-symbols-outlined text-[#bef264]">account_tree</span>
        PortalX
      </div>
      <div class="flex gap-2">
        <button class="material-symbols-outlined text-on-surface-variant hover:text-[#bef264] transition-colors cursor-pointer py-1 px-2 text-lg">
          help
        </button>
      </div>
    </header>

    <main class="flex-grow flex items-center justify-center px-6 py-24 relative z-10 font-sans">
      <div class="w-full max-w-[440px] bg-[#1a1c1c] p-8 lg:p-10 rounded-xl border border-white/[0.08]">
        <div class="text-center mb-10">
          <h1 class="font-display text-3xl font-semibold mb-2 text-primary">Welcome Back</h1>
          <p class="text-sm text-on-surface-variant">Sign in to access your command center</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-2">
            <label class="font-mono text-xs text-on-surface-variant block uppercase tracking-wider">Email Address</label>
            <input
              v-model="email"
              type="email"
              required
              placeholder="name@company.com"
              class="w-full bg-[#272929] border border-transparent rounded-lg px-4 py-3 text-sm text-on-surface placeholder:text-on-surface-variant/40 focus:outline-none focus:ring-1 focus:ring-[#bef264] transition-all"
            />
          </div>

          <div class="space-y-2">
            <label class="font-mono text-xs text-on-surface-variant block uppercase tracking-wider">Password</label>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="••••••••"
                class="w-full bg-[#272929] border border-transparent rounded-lg px-4 py-3 text-sm text-[#e3e2e2] placeholder:text-on-surface-variant/40 focus:outline-none focus:ring-1 focus:ring-[#bef264] pr-12 transition-all"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-[#bef264] transition-colors"
              >
                <span class="material-symbols-outlined text-lg leading-none">
                  {{ showPassword ? 'visibility_off' : 'visibility' }}
                </span>
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between py-1">
            <label class="flex items-center gap-3 cursor-pointer group">
              <div class="relative w-5 h-5">
                <input
                  v-model="rememberMe"
                  type="checkbox"
                  class="peer sr-only"
                />
                <div class="w-5 h-5 border-2 border-[#272929] rounded bg-[#272929] peer-checked:bg-[#bef264] peer-checked:border-[#bef264] transition-all"></div>
                <span class="material-symbols-outlined absolute inset-0 text-md text-[#131f00] font-bold flex items-center justify-center opacity-0 peer-checked:opacity-100">
                  check
                </span>
              </div>
              <span class="text-sm text-on-surface-variant group-hover:text-on-surface transition-colors">Remember me</span>
            </label>
            <a href="#" class="text-sm text-[#bef264] hover:underline hover:text-[#a4d64c] transition-all">Forgot password?</a>
          </div>

          <div v-if="authStore.error" class="rounded-md bg-red-900/20 p-4 border border-red-900/50">
            <div class="flex">
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-400">{{ authStore.error }}</h3>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full bg-[#bef264] text-[#131f00] hover:bg-[#a4d64c] font-display text-lg py-3.5 rounded-lg font-bold flex items-center justify-center transition-all cursor-pointer transform active:scale-95 duration-100 uppercase tracking-wide disabled:opacity-50"
          >
            <span v-if="authStore.isLoading" class="material-symbols-outlined animate-spin mr-2">progress_activity</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <!-- Alternative methods -->
        <div class="relative my-8">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/[0.05]"></div>
          </div>
          <div class="relative flex justify-center text-xs text-on-surface-variant font-mono uppercase">
            <span class="bg-[#1a1c1c] px-4">Or continue with</span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <button 
            type="button" 
            @click="handleDemoLogin('freelancer@example.com')"
            class="flex items-center justify-center gap-2 bg-[#272929] border border-white/[0.05] text-on-surface hover:bg-[#343535] py-3 rounded-lg transition-colors cursor-pointer active:scale-95"
            title="Login as test user"
          >
            <span class="font-sans font-medium text-sm text-[#e3e2e2]">Google</span>
          </button>
          <button 
            type="button" 
            @click="handleDemoLogin('freelancer2@example.com')"
            class="flex items-center justify-center gap-2 bg-[#272929] border border-white/[0.05] text-on-surface hover:bg-[#343535] py-3 rounded-lg transition-colors cursor-pointer active:scale-95"
            title="Login as alternate user"
          >
            <span class="font-sans font-medium text-sm text-[#e3e2e2]">GitHub</span>
          </button>
        </div>

        <!-- Direct Magic Client Access Bypassing Login -->
        <div class="mt-8 pt-6 border-t border-white/[0.05] text-center">
          <p class="text-xs text-on-surface-variant font-mono uppercase tracking-wider mb-2.5">Client Portal Simulation</p>
          <div class="bg-[#bef264]/[0.03] border border-[#bef264]/10 rounded-lg p-4 text-left transition-all hover:bg-[#bef264]/[0.05]">
            <p class="text-[11px] text-gray-400 mb-3 leading-relaxed">
              Clients access a dedicated premium portal path with <strong class="text-white">NO password or sign-in required</strong>.
            </p>
            <button
              type="button"
              @click="handleMagicLink"
              class="w-full py-2.5 rounded-md bg-[#212323] hover:bg-[#bef264] hover:text-[#131f00] text-[#e3e2e2] text-xs font-bold font-mono tracking-wide transition-all duration-150 cursor-pointer text-center flex items-center justify-center gap-2 border border-white/5 uppercase"
            >
              <span class="material-symbols-outlined text-sm">vpn_key</span>
              Bypass and Enter Magic Link Portal
            </button>
            <span class="text-[9px] text-[#bef264]/50 font-mono block text-center mt-2 lowercase">
              Simulates visiting URL /portal/[token]
            </span>
          </div>
        </div>
      </div>
    </main>

    <footer class="fixed bottom-0 w-full flex flex-col md:flex-row justify-between items-center px-6 py-4 bg-surface-container-lowest text-xs text-on-surface-variant border-t border-white/[0.05]">
      <div class="order-2 md:order-1 opacity-60">
        © 2026 PortalX. All rights reserved.
      </div>
      <div class="flex gap-4 order-1 md:order-2 mb-2 md:mb-0">
        <a class="hover:text-[#bef264] transition-colors" href="#">Privacy Policy</a>
        <a class="hover:text-[#bef264] transition-colors" href="#">Terms of Service</a>
        <a class="hover:text-[#bef264] transition-colors" href="#">Support</a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from '#app'
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: false
})

const authStore = useAuthStore()
const router = useRouter()

const email = ref('freelancer@example.com')
const password = ref('password123')
const showPassword = ref(false)
const rememberMe = ref(true)

const handleLogin = async () => {
  const success = await authStore.login({
    email: email.value,
    password: password.value
  })

  if (success) {
    router.push('/')
  }
}

const handleDemoLogin = async (demoEmail) => {
  email.value = demoEmail
  password.value = 'password123'
  await handleLogin()
}

const handleMagicLink = () => {
  const token = prompt('Enter a magic link token to simulate a client visit (if known):', 'nexus-vanguard-token-abc')
  if (token) {
    router.push(`/portal/${token}`)
  }
}
</script>
