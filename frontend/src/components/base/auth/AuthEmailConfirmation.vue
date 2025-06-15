<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/store/auth'

// Utilities
import axios from 'axios'
import { toast } from 'vue3-toastify'

const { t } = useI18n()
const store = useAuthStore()

const resentActivation = async () => {
  if (!store.registrationEmail) return

  try {
    await axios.post('/api/v1/users/resend_activation/', {
      email: store.registrationEmail,
    })

    toast.success(t('toasts.emailActivationResent'))
  } catch (error) {
    console.error(error)
    toast.error(t('toasts.somethingWrong'))
  }
}
</script>

<template>
  <v-alert class="text-body-1 mb-8">
    <p class="mb-4">{{ t('auth.emailConfirmation.thankYou') }}</p>
    <p class="mb-4">
      {{
        t('auth.emailConfirmation.confirmationSent', {
          email: store.registrationEmail,
        })
      }}
    </p>
    <p class="text-body-2">
      {{ t('auth.emailConfirmation.verificationWarning') }}
    </p>
    <p class="text-body-2 mb-4">
      {{ t('auth.emailConfirmation.spamNotice') }}
    </p>
    <p>
      {{ t('auth.emailConfirmation.resentPrompt') }}
      <v-btn
        class="text-body-1"
        color="info"
        :text="t('buttons.resentEmail')"
        variant="text"
        size="sm"
        @click="resentActivation"
      />
    </p>
  </v-alert>
  <v-btn
    :text="t('buttons.login')"
    @click="store.authMode = 'login'"
    @keydown.enter=""
    block
    color="info"
    variant="tonal"
    class="mb-4"
  />
</template>
