<script setup lang="ts">
// Components
import AuthDialog from '@/components/base/auth/AuthDialog.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'

// Utilities
import { shallowRef } from 'vue'

const authStore = useAuthStore()
const { t } = useI18n()

const items = [
  { to: '/profile', id: 'profile' },
  { to: '/pricing', id: 'planAndPricing' },
  { to: '/notifications', id: 'notifications' },
  { to: '/helpcenter', id: 'helpCenter' },
]
const dialog = shallowRef(false)
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
                v-if="authStore.profile?.is_staff"
                :to="{ name: 'admin' }"
                :title="t('header.adminPanel')"
              />
              <v-list-item
                v-for="item in items"
                :key="item.id"
                :title="t(`header.${item.id}`)"
                :to="item.to"
              />
              <v-divider />
              <v-list-item
                @click="authStore.logout()"
                :title="t('header.logout')"
              />
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
