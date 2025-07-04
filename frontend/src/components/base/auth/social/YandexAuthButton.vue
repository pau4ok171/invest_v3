<script setup lang="ts">
// Components
import YandexIcon from '@/components/icons/YandexIcon.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'

// Utilities
import { onMounted, onUnmounted } from 'vue'
import axios from 'axios'

// Types
import type { LoginResponse } from '@/store/auth'

const authStore = useAuthStore()
const { t } = useI18n()

const yandexLogin = () => {
  const width = 600
  const height = 700
  const left = (window.screen.width - width) / 2
  const top = (window.screen.height - height) / 2

  const clientId = '11f9fcbe5d544efcb15c3817419334bf'
  const redirectUri = 'http://localhost:5173/auth/yandex/login/callback/'

  const url = `https://oauth.yandex.ru/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}`

  const popup = window.open(
    '',
    'yandexAuth',
    `width=${width},height=${height},top=${top},left=${left},toolbar=0,menubar=0,location=0`
  )

  if (!popup) return

  localStorage.setItem('yandex_popup', 'open')

  popup.location.href = url
}

const processAuth = async (code: string) => {
  try {
    const response = await axios.post<LoginResponse>(
      '/api/v1/auth/yandex/',
      {
        code,
      },
      {
        withCredentials: true,
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      }
    )

    await authStore.setUserProfile(response.data)
  } catch (error) {
    console.error(error)
  }
}

const checkAuth = (event: StorageEvent) => {
  if (event.key === 'yandex_auth_response') {
    const data = JSON.parse(event.newValue || '{}')

    if (data.code) {
      processAuth(data.code)
      localStorage.removeItem('yandex_auth_response')
    }
  }
}

onMounted(() => {
  window.addEventListener('storage', checkAuth)
})

onUnmounted(() => {
  window.removeEventListener('storage', checkAuth)
})
</script>

<template>
  <v-btn class="text-none text-body-1" variant="tonal" color="info" @click="yandexLogin">
    <template #prepend>
      <v-avatar size="20">
        <yandex-icon />
      </v-avatar>
    </template>
    {{ t('buttons.loginWithYandex') }}
  </v-btn>
</template>
