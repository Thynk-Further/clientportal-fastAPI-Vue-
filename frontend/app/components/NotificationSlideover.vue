<template>
  <div>
    <!-- Backdrop -->
    <transition
      enter-active-class="transition-opacity ease-linear duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity ease-linear duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="isOpen" class="fixed inset-0 bg-black/50 z-50" @click="close"></div>
    </transition>

    <!-- Slide-over panel -->
    <transition
      enter-active-class="transition ease-in-out duration-300 transform"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition ease-in-out duration-300 transform"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <div
        v-if="isOpen"
        class="fixed inset-y-0 right-0 max-w-md w-full bg-[#171717] border-l border-white/5 z-50 shadow-2xl flex flex-col"
      >
        <div class="px-6 py-4 border-b border-white/5 flex items-center justify-between shrink-0">
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            Notifications
            <span v-if="unreadCount > 0" class="bg-[#bef264] text-[#131f00] text-xs font-bold px-2 py-0.5 rounded-full">
              {{ unreadCount }}
            </span>
          </h2>
          <div class="flex items-center gap-2">
            <button 
              v-if="unreadCount > 0" 
              @click="markAllRead" 
              class="text-xs text-gray-400 hover:text-white transition-colors px-2 py-1"
            >
              Mark all read
            </button>
            <button @click="close" class="text-gray-400 hover:text-white p-1 rounded-md hover:bg-white/5 transition-colors">
              <span class="material-symbols-outlined text-[20px]">close</span>
            </button>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-2">
          <div v-if="loading" class="text-center py-8 text-gray-400 text-sm">
            Loading...
          </div>
          <div v-else-if="notifications.length === 0" class="text-center py-12 text-gray-500 flex flex-col items-center gap-3">
            <span class="material-symbols-outlined text-4xl opacity-50">notifications_off</span>
            <p class="text-sm">You have no notifications yet.</p>
          </div>
          <div 
            v-else 
            v-for="notification in notifications" 
            :key="notification.id"
            :class="[
              'p-4 rounded-xl border transition-colors flex flex-col gap-2',
              notification.read_at ? 'bg-white/[0.02] border-transparent' : 'bg-[#1e2020] border-[#bef264]/20'
            ]"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <p :class="['text-sm font-semibold truncate', notification.read_at ? 'text-gray-300' : 'text-white']">
                  {{ notification.title }}
                </p>
                <p class="text-xs text-gray-400 mt-1 line-clamp-2">
                  {{ notification.message }}
                </p>
              </div>
              <div v-if="!notification.read_at" class="w-2 h-2 rounded-full bg-[#bef264] shrink-0 mt-1"></div>
            </div>
            <div class="flex items-center justify-between mt-2">
              <span class="text-[10px] text-gray-500 font-mono">{{ formatDate(notification.created_at) }}</span>
              <NuxtLink v-if="notification.link_url" :to="notification.link_url" class="text-xs text-[#bef264] hover:underline font-semibold" @click.stop="markAsRead(notification.id)">
                View details
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  isPortal: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'update:unreadCount'])

const router = useRouter()
const notifications = ref([])
const unreadCount = ref(0)
const loading = ref(false)

const baseUrl = computed(() => props.isPortal ? '/api/v1/portal/notifications' : '/api/v1/notifications')

const fetchNotifications = async () => {
  loading.value = true
  try {
    const { $api } = useNuxtApp()
    const res = await $api(baseUrl.value)
    notifications.value = res.items
    unreadCount.value = res.unread_count
    emit('update:unreadCount', unreadCount.value)
  } catch (err) {
    console.error('Failed to fetch notifications', err)
  } finally {
    loading.value = false
  }
}

const markAsRead = async (id) => {
  const notif = notifications.value.find(n => n.id === id)
  if (notif && !notif.read_at) {
    notif.read_at = new Date().toISOString()
    unreadCount.value = Math.max(0, unreadCount.value - 1)
    emit('update:unreadCount', unreadCount.value)
    try {
      const { $api } = useNuxtApp()
      await $api(`${baseUrl.value}/${id}/read`, { method: 'POST' })
    } catch (err) {
      console.error('Failed to mark read', err)
    }
  }
}

const markAllRead = async () => {
  notifications.value.forEach(n => {
    if (!n.read_at) n.read_at = new Date().toISOString()
  })
  unreadCount.value = 0
  emit('update:unreadCount', 0)
  try {
    const { $api } = useNuxtApp()
    await $api(`${baseUrl.value}/read-all`, { method: 'POST' })
  } catch (err) {
    console.error('Failed to mark all read', err)
  }
}

const handleNotificationClick = (notification) => {
  markAsRead(notification.id)
  if (notification.link_url) {
    router.push(notification.link_url)
    close()
  }
}

const close = () => {
  emit('close')
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleString()
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    fetchNotifications()
  }
})

// For polling unread count when closed, or we rely on websockets!
// Since we have websockets for projects/users, the parent layout can update the count,
// or we can expose a method to add a new notification to the list.
defineExpose({
  fetchNotifications,
  addNotification: (n) => {
    notifications.value.unshift(n)
    unreadCount.value++
    emit('update:unreadCount', unreadCount.value)
  }
})
</script>
