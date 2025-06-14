<script setup lang="ts">
// Components
import { BaseFlag } from '@/components/UI/BaseFlag'

// Composables
import { computed, watch } from 'vue'
import { useLocale } from 'vuetify'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/store/auth'

// Utilities
import axios from 'axios'

const langs = [
  { id: 'en', title: 'English', iso: 'gb' },
  { id: 'ru', title: 'Русский', iso: 'ru' },
  { id: 'fr', title: 'Français', iso: 'fr' },
  { id: 'es', title: 'Español', iso: 'es' },
  { id: 'de', title: 'Deutsch', iso: 'de' },
  { id: 'pl', title: 'Polski', iso: 'pl' },
  { id: 'it', title: 'Italiano', iso: 'it' },
]

const authStore = useAuthStore()
const { current } = useLocale()
const { locale, t } = useI18n()

// Текущая локаль из профиля или сохраненная в localeStorage
const currentLocale = computed({
  get: () =>
    [authStore.profile?.locale || localStorage.getItem('locale') || 'en'],
  set: async (newLocale: [string]) => {
    await changeLocale(newLocale[0])
  },
})

// Инициализация локали при загрузке
current.value = currentLocale.value[0]
locale.value = currentLocale.value[0]

const changeLocale = async (newLocale: string) => {
  try {
    // Обновляем локально
    current.value = newLocale
    locale.value = newLocale
    localStorage.setItem('locale', newLocale)

    // Обновляем в хранилище (если пользователь авторизован)
    if (authStore.isAuthenticated) {
      authStore.profile.locale = newLocale
      await updateLocale(newLocale)
    }
  } catch (error) {
    console.error('Failed to change locale:', error)
  }
}

const updateLocale = async (newLocale: string) => {
  try {
    await axios.patch('/api/v1/profile/me/', { locale: newLocale })
  } catch (error) {
    console.error('Failed to update locale on server:', error)
    throw error
  }
}

watch(
  () => authStore.profile?.locale,
  async (newLocale) => {
    if (newLocale && newLocale !== locale.value) {
      await changeLocale(currentLocale.value[0])
    }
  }
)
</script>

<template>
  <v-menu>
    <template #activator="{ props }">
      <v-btn v-bind="props" icon="$iLang" variant="text" rounded="lg" />
    </template>
    <template #default>
      <v-card>
        <v-list
          v-model:selected="currentLocale"
          slim
          nav
          density="compact"
          mandatory
        >
          <v-list-subheader
            class="text-high-emphasis text-uppercase font-weight-black"
          >
            {{ t('header.translations') }}
          </v-list-subheader>
          <v-list-item
            v-for="item in langs"
            :key="item.id"
            :title="item.title"
            :value="item.id"
            rounded
          >
            <template #prepend>
              <base-flag :code="item.iso" />
            </template>
          </v-list-item>
        </v-list>
      </v-card>
    </template>
  </v-menu>
</template>
