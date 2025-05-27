<script setup lang="ts">
// Components
import AuthLoginForm from '@/components/base/auth/AuthLoginForm.vue'
import AuthRegistrationForm from '@/components/base/auth/AuthRegistrationForm.vue'

// Composables
import { useAuthStore } from '@/store/auth'

// Utilities
import { onUnmounted, shallowRef } from 'vue'

const store = useAuthStore()
const dialog = shallowRef(false)

onUnmounted(() => {
  store.authMode = 'login'
})
</script>

<template>
  <v-dialog activator="parent" max-width="700" v-model="dialog">
    <v-card title="Finargo">
      <template #append>
        <v-btn
          icon="$close"
          density="compact"
          variant="text"
          @click="dialog = false"
        />
      </template>
      <v-card-item>
        <auth-login-form v-if="store.authMode === 'login'" />
        <auth-registration-form v-else />
      </v-card-item>
    </v-card>
  </v-dialog>
</template>
