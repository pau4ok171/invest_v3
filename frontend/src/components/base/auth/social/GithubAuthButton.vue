<script setup lang="ts">
// Components
import GithubIcon from '@/components/icons/GithubIcon.vue'

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

const githubLogin = () => {
  const width = 600
  const height = 700
  const left = (window.screen.width - width) / 2
  const top = (window.screen.height - height) / 2

  const clientId = 'Ov23li94LeewLMKCCCwu'
  const redirectUri = `http://localhost:5173/auth/github/login/callback/`
  const scope = 'user:email'

  const url = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`

  const popup = window.open(
    '',
    'githubAuth',
    `width=${width},height=${height},top=${top},left=${left},toolbar=0,menubar=0,location=0`
  )

  if (!popup) return

  localStorage.setItem('github_popup', 'open')

  popup.location.href = url
}

const processAuth = async (code: string) => {
  try {
    const response = await axios.post<LoginResponse>(
      '/api/v1/auth/github/',
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
  if (event.key === 'github_auth_response') {
    const data = JSON.parse(event.newValue || '{}')

    if (data.code) {
      processAuth(data.code)
      localStorage.removeItem('github_auth_response')
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
  <v-btn class="text-none text-body-1" variant="tonal" color="info" @click="githubLogin">
    <template #prepend>
      <v-avatar size="20">
        <github-icon />
      </v-avatar>
    </template>
    {{ t('buttons.loginWithGithub') }}
  </v-btn>
</template>
