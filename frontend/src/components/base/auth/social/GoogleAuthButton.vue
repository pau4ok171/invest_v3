<script setup lang="ts">
// Components
import GoogleIcon from '@/components/icons/GoogleIcon.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'
import { googleTokenLogin } from 'vue3-google-login'

// Utilities
import axios from 'axios'

// Types
import type { LoginResponse } from '@/store/auth'

const authStore = useAuthStore()
const { t } = useI18n()

const googleLogin = async () => {
  googleTokenLogin().then(async (googleResponse) => {
    try {
      const response = await axios.post<LoginResponse>(
        'api/v1/auth/google/',
        {
          access_token: googleResponse.access_token,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        }
      )
      await authStore.setUserProfile(response.data)
    } catch (e) {
      console.log(e)
    }
  })
}
</script>

<template>
  <v-btn class="text-none text-body-1" variant="tonal" color="info" @click="googleLogin">
    <template #prepend>
      <v-avatar size="20">
        <google-icon />
      </v-avatar>
    </template>
    {{ t('buttons.loginWithGoogle') }}
  </v-btn>
</template>
