<script setup lang="ts">
// Static
import { type Language, LANGUAGES } from '@/assets/static/common'

// Composables
import {
  useAuthStore,
  type UserProfilePatchData,
  type UserProfileResponse,
} from '@/store/auth'
import { useI18n } from 'vue-i18n'
import { useTranslations } from '@/composables/translations'

// Utilities
import { computed, ref, shallowRef, watch } from 'vue'
import { DateTime } from 'ts-luxon'
import axios from 'axios'
import { toast } from 'vue3-toastify'

// Types
import type { UserProfile } from '@/store/auth'
import type { CountryState, CurrencyState } from '@/store/companyList/types'

const authStore = useAuthStore()
const profile = computed<UserProfile | null>(() => authStore.profile)
const newProfile = profile.value
  ? ref<UserProfile>({ ...profile.value })
  : ref(null)
const { t, locale } = useI18n()
const { getTranslation } = useTranslations()

const loading = shallowRef(false)
const dialog = shallowRef(false)
const colorDialog = shallowRef(false)
const saveDialog = shallowRef(false)
const wasChanged = computed<boolean>(() => {
  if (!profile.value || !newProfile.value) return false

  if (avatarFile.value) return true

  const keys = Object.keys(profile.value) as Array<keyof UserProfile>

  return keys.some((key) => {
    const oldVal = profile.value![key]
    const newVal = newProfile.value![key]

    if (Array.isArray(oldVal) && Array.isArray(newVal)) {
      return JSON.stringify(oldVal) !== JSON.stringify(newVal)
    }

    return oldVal !== newVal
  })
})

// Community Profile
const avatarFile = ref<File | null>(null)
const bgStyles = computed(() => {
  if (!newProfile.value) return ''
  return `background-color: ${newProfile.value.bannerColor || '#FFFFFF'}`
})
const aboutMeLength = computed(() =>
  newProfile.value ? newProfile.value.aboutMe.length : 0
)
const avatarURL = computed<string | undefined>(() => {
  if (avatarFile.value) {
    return avatarFile.value?.type.startsWith('image')
      ? URL.createObjectURL(avatarFile.value)
      : undefined
  }
  return newProfile.value ? newProfile.value.avatar || undefined : undefined
})

const deleteAvatar = () => {
  if (!newProfile.value) return

  newProfile.value.avatar = null
}

// Preferences
const countries = computed(() => {
  if (!authStore.countryOptions.length) return []

  return authStore.countryOptions
    .map((c) => {
      const title = getTranslation(c.translations, 'name')
      return {
        ...c,
        title,
      }
    })
    .sort((a, b) => a.title.localeCompare(b.title))
})
const selectedCountry = computed({
  get: () =>
    countries.value.find((c) => c.key === newProfile.value?.countryCode),
  set: (newValue: CountryState) => {
    if (!newProfile.value) return
    newProfile.value.countryCode = newValue.key
  },
})

const currencies = computed(() => {
  if (!authStore.currencyOptions.length) return []

  return authStore.currencyOptions
    .map((c) => {
      const title = getTranslation(c.translations, 'name')
      return {
        ...c,
        title,
      }
    })
    .sort((a, b) => a.title.localeCompare(b.title))
})
const selectedCurrency = computed({
  get: () =>
    currencies.value.find((c) => c.key === newProfile.value?.currencyCode),
  set: (newValue: CurrencyState) => {
    if (!newProfile.value) return
    newProfile.value.currencyCode = newValue.key
  },
})

const languages = [...LANGUAGES]
const selectedLanguage = computed({
  get: () => languages.find((l) => l.id === newProfile.value?.languageCode),
  set: (newValue: Language) => {
    if (!newProfile.value) return
    newProfile.value.languageCode = newValue.id
  },
})

// Account Details
const registrationDate = computed(() => {
  if (!newProfile.value) return '-'
  return DateTime.fromMillis(newProfile.value.registrationDate).toFormat(
    'DDD',
    {
      locale: locale.value,
    }
  )
})

// Main Functions
const submitProfileUpdate = async () => {
  // Prepare Form Data
  const data = newProfile.value
  if (!data) return

  const formData = new FormData()
  formData.append('first_name', data.firstName)
  formData.append('last_name', data.familyName)
  formData.append('display_name', data.displayName)
  formData.append('locale', data.languageCode)
  formData.append('country_iso', data.countryCode)
  formData.append('currency_iso', data.currencyCode)
  formData.append('bio', data.aboutMe)
  formData.append('banner_color', data.bannerColor)
  if (avatarFile.value && avatarFile.value.type.startsWith('image')) {
    formData.append('avatar', avatarFile.value)
  } else if (!newProfile.value.avatar) {
    formData.append('avatar', '')
  }
  try {
    loading.value = true
    // Submit Form to Server
    const response = await axios.patch<UserProfileResponse>(
      'api/v1/auth/user/',
      formData
    )
    // Set profile
    authStore.setUserProfile({ user: response.data })
    // Reset newProfile
    resetComponent()

    toast.success(t('toasts.profileSaved'), {
      position: 'top-center',
      autoClose: 3000,
    })
    // successSnack.value = true
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const closeProfileDialog = (preventClose: boolean = true) => {
  if (preventClose && wasChanged.value) {
    saveDialog.value = true
    return
  }

  dialog.value = false
}

const resetComponent = () => {
  avatarFile.value = null
  saveDialog.value = false
  resetNewProfile()
}
const resetNewProfile = () => {
  newProfile.value = profile.value ? { ...profile.value } : null
}

watch(dialog, (value) => {
  if (!value) {
    resetComponent()
  }
})
</script>

<template>
  <v-dialog activator="parent" max-width="1200" v-model="dialog" persistent>
    <v-toolbar color="surface" flat class="rounded-t-lg px-4">
      <v-toolbar-title>{{ t('profile.profile') }}</v-toolbar-title>
      <v-spacer />
      <v-btn
        icon="$close"
        density="comfortable"
        variant="text"
        rounded="lg"
        @click="closeProfileDialog"
      />
    </v-toolbar>
    <v-card class="rounded-t-0">
      <v-card-item>
        <v-form v-if="newProfile">
          <v-card :loading="loading">
            <v-row>
              <v-col cols="6">
                <v-card-item :title="t('profile.communityProfile')">
                  <v-text-field
                    v-model="newProfile.displayName"
                    :label="t('labels.displayName')"
                    variant="outlined"
                    class="mb-2 mt-8"
                    color="info"
                    :disabled="loading"
                  />

                  <v-divider class="mb-8" />

                  <v-file-input
                    :prepend-icon="null as unknown as undefined"
                    v-model="avatarFile"
                    :label="t('labels.avatar')"
                    variant="outlined"
                    class="profile-form__file-input my-2"
                    color="info"
                    show-size
                    clearable
                    chips
                    accept="image/*"
                    :disabled="loading"
                  />

                  <v-btn
                    v-if="!avatarFile && newProfile.avatar"
                    @click="deleteAvatar"
                    color="error"
                    class="text-capitalize"
                    :text="t('buttons.deleteAvatar')"
                    variant="outlined"
                  />

                  <v-divider class="my-8" />

                  <span class="v-label mb-4 ml-4">{{
                    t('labels.bannerColor')
                  }}</span>

                  <v-dialog
                    v-model="colorDialog"
                    :scrim="true"
                    width="fit-content"
                    :close-on-content-click="false"
                    offset="180"
                    location="end"
                    location-strategy="connected"
                    :disabled="loading"
                  >
                    <template #activator="{ props: activatorProps }">
                      <v-card
                        v-bind="activatorProps"
                        width="100"
                        height="50"
                        :color="newProfile.bannerColor"
                        class="color-preview-card"
                      >
                        <template #append>
                          <v-icon class="edit-icon" size="20" icon="$edit" />
                        </template>
                      </v-card>
                    </template>
                    <v-card>
                      <v-card-item>
                        <v-color-picker
                          v-model="newProfile.bannerColor"
                          :canvas-height="100"
                          :modes="['hex']"
                          elevation="0"
                        />
                      </v-card-item>
                    </v-card>
                  </v-dialog>

                  <v-divider class="my-8" />

                  <v-textarea
                    v-model="newProfile.aboutMe"
                    :label="t('labels.aboutMe')"
                    variant="outlined"
                    class="my-2"
                    color="info"
                    :counter-value="() => 190 - aboutMeLength"
                    auto-grow
                    rows="3"
                    persistent-counter
                    :disabled="loading"
                  />

                  <v-divider class="my-8" />
                </v-card-item>
              </v-col>
              <v-col cols="6">
                <v-card-item :title="t('profile.preview')">
                  <v-card
                    class="mt-8"
                    color="background"
                    width="75%"
                    height="200"
                  >
                    <div class="h-50" :style="bgStyles" />
                    <div class="user-preview__avatar-wrapper">
                      <v-avatar size="70">
                        <v-img v-if="avatarURL" :src="avatarURL" cover />
                      </v-avatar>
                    </div>
                    <div class="user-preview__wrapper mt-4">
                      <div class="text-body-1 text-truncate">
                        {{ newProfile.displayName || 'Investor' }}
                      </div>
                    </div>
                  </v-card>
                </v-card-item>
              </v-col>
            </v-row>

            <v-card-item :title="t('profile.preferences')">
              <v-row class="mt-4">
                <v-col cols="6">
                  <v-select
                    v-model="selectedLanguage"
                    :items="languages"
                    item-title="title"
                    item-key="id"
                    return-object
                    :label="t('labels.language')"
                    variant="outlined"
                    class="my-2"
                    color="info"
                    :disabled="loading"
                  />

                  <v-divider class="mb-8" />

                  <v-select
                    v-model="selectedCountry"
                    :items="countries"
                    item-title="title"
                    item-key="key"
                    return-object
                    :label="t('labels.country')"
                    variant="outlined"
                    class="my-2"
                    color="info"
                    :disabled="loading"
                  />

                  <v-divider class="mb-8" />

                  <v-select
                    v-model="selectedCurrency"
                    :items="currencies"
                    item-title="title"
                    item-key="key"
                    return-object
                    :label="t('labels.currency')"
                    variant="outlined"
                    class="my-2"
                    color="info"
                    :disabled="loading"
                  />

                  <v-divider class="mb-8" />
                </v-col>
              </v-row>
            </v-card-item>

            <v-card-item :title="t('profile.accountDetails')">
              <v-row class="mt-4">
                <v-col cols="6">
                  <div class="d-flex flex-column">
                    <span class="text-button text-medium-emphasis">{{
                      t('labels.loginMethod')
                    }}</span>
                    <span class="text-subtitle-1 text-capitalize">
                      {{ newProfile.loginMethod }}
                    </span>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="d-flex flex-column">
                    <span class="text-button text-medium-emphasis">
                      {{ t('labels.registrationDate') }}
                    </span>
                    <span class="text-subtitle-1">{{ registrationDate }}</span>
                  </div>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6">
                  <v-text-field
                    v-model="newProfile.firstName"
                    :label="t('labels.firstName')"
                    variant="outlined"
                    class="my-2"
                    color="info"
                    :disabled="loading"
                  />

                  <v-divider class="mb-8" />

                  <v-text-field
                    v-model="newProfile.familyName"
                    :label="t('labels.familyName')"
                    variant="outlined"
                    class="my-2"
                    color="info"
                    :disabled="loading"
                  />

                  <v-divider class="mb-16" />
                </v-col>
              </v-row>
            </v-card-item>

            <v-snackbar
              :model-value="wasChanged"
              :close-on-content-click="false"
              :close-on-back="false"
              :timeout="-1"
              :text="t('profile.saveText')"
              :attach="true"
              color="surface-bright"
              variant="elevated"
              width="max-content"
              max-width="100%"
              transition="slide-y-reverse-transition"
            >
              <template #actions>
                <v-btn
                  :disabled="loading"
                  variant="plain"
                  class="text-capitalize"
                  :text="t('buttons.reset')"
                  @click="resetComponent"
                />
                <v-btn
                  variant="flat"
                  class="text-capitalize"
                  color="success"
                  :text="t('buttons.saveModifications')"
                  @click="submitProfileUpdate"
                  :loading="loading"
                />
              </template>
            </v-snackbar>
          </v-card>
        </v-form>
      </v-card-item>
    </v-card>

    <v-dialog v-model="saveDialog" max-width="600" persistent>
      <v-card title="">
        <v-card-text>
          {{ t('profile.preventText') }}
        </v-card-text>
        <v-card-actions>
          <v-btn
            class="text-capitalize"
            color="error"
            :text="t('buttons.closeWithoutSaving')"
            @click="closeProfileDialog(false)"
          />
          <v-btn
            variant="tonal"
            color="success"
            :text="t('buttons.no')"
            @click="saveDialog = false"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<style lang="scss" scoped>
:global(.profile-form__file-input > .v-input__control) {
  cursor: pointer;
}
.user-preview__wrapper {
  position: absolute;
  margin-left: 24px;
  top: 75%;
  transform: translateY(-50%);
  width: calc(100% - 48px);
}
.user-preview__avatar-wrapper {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 24px;
  margin-right: 24px;
  top: 50%;
  transform: translateY(-50%);
  width: 80px;
  height: 80px;
  background-color: rgb(var(--v-theme-background));
  border-radius: 50%;
}
.edit-icon {
  opacity: 0;
  transition: opacity 0.2s ease;
}
.color-preview-card {
  position: relative;

  &:hover .edit-icon {
    opacity: 1;
  }
}
</style>
