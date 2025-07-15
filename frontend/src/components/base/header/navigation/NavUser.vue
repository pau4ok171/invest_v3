<script setup lang="ts">
// Components
import AuthDialog from '@/components/base/auth/AuthDialog.vue'
import ProfileDialog from '@/components/base/auth/ProfileDialog.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

const authStore = useAuthStore()
const profile = computed(() => authStore.profile)
const { t } = useI18n()

const items = [
  { to: '/pricing', id: 'planAndPricing' },
  { to: '/notifications', id: 'notifications' },
  { to: '/helpcenter', id: 'helpCenter' },
]

const avatarInitial = computed(() => {
  if (!profile.value) return 'I'
  return profile.value.username.charAt(0).toUpperCase()
})

const avatarColor = computed(() => {
  const colors = ['primary', 'secondary', 'success', 'error', 'warning', 'info']

  if (!profile.value) return colors[0]

  const index = profile.value.username.length % colors.length
  return colors[index]
})
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
            <v-card-item v-if="profile">
              <div class="d-flex flex-column align-center ga-3 mt-4">
                <v-avatar
                  v-if="profile.avatar"
                  :image="profile.avatar"
                  :size="72"
                />

                <v-avatar :color="avatarColor" v-else :size="72">
                  <span class="text-h5">{{ avatarInitial }}</span>
                </v-avatar>

                <span>{{ profile.username }}</span>
                <span class="text-medium-emphasis">{{ profile.email }}</span>
                <v-btn class="text-capitalize" color="info" variant="outlined">
                  <profile-dialog />
                  {{ t('buttons.editProfile') }}
                </v-btn>
              </div>
            </v-card-item>
            <v-list>
              <v-list-item
                v-if="authStore.profile?.isStaff"
                base-color="info"
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
                base-color="error"
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
