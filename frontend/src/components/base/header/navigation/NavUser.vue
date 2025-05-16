<script setup lang="ts">
// Components
import AuthDialog from '@/components/base/auth/AuthDialog.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'

// Utilities
import { ref, shallowRef } from 'vue'
import axios from 'axios'

const authStore = useAuthStore()
const { t } = useI18n()

const items = ref([
  { title: 'Profile', to: '/profile', id: 'profile' },
  { title: 'Plan & Pricing', to: '/pricing', id: 'pricing' },
  { title: 'Notifications', to: '/notifications', id: 'notifications' },
  { title: 'HelpCenter', to: '/helpcenter', id: 'help' },
])
const dialog = shallowRef(false)

function onLogout() {
  axios.defaults.headers.common['Authorization'] = ''

  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('userid')

  authStore.token = ''
  authStore.userInfo = {
    first_name: '',
    is_anonymous: true,
    is_staff: false,
    last_name: '',
    stage_in_days: 0,
  }
}
</script>

<template>
  <div class="nav-user__wrapper">
    <template v-if="authStore.isAuthenticated">
      <v-menu>
        <template #activator="{ props }">
          <v-btn v-bind="props" icon="$iUser" variant="text" rounded="lg" />
        </template>
        <template #default>
          <v-card>
            <v-list>
              <v-list-item
                v-if="authStore.userInfo.is_staff"
                :to="{ name: 'admin' }"
                title="Admin Panel"
              />
              <v-list-item
                v-for="item in items"
                :key="item.id"
                :title="item.title"
                :to="item.to"
              />
              <v-divider />
              <v-list-item @click="onLogout" title="Logout" />
            </v-list>
          </v-card>
        </template>
      </v-menu>
    </template>

    <template v-else>
      <v-btn color="info" variant="outlined">
        <auth-dialog />
        {{ t('buttons.login') }}
      </v-btn>
    </template>
  </div>
</template>

<style>
.nav-user__wrapper {
  display: flex;
  justify-content: center;
  min-width: 90px;
}
</style>
