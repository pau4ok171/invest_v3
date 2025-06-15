<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'
import { useVuelidate } from '@vuelidate/core'
import { useAuthStore } from '@/store/auth'

// Utilities
import { computed, reactive, ref, shallowRef } from 'vue'
import axios from 'axios'
import { isObjectLike } from 'lodash'
import { toast } from 'vue3-toastify'
import { i18n } from '@/i18n/i18n'

// Validators
import { required, emailField } from '@/common/vuelidate/validators'
import { helpers } from '@vuelidate/validators'

interface FormError {
  title: string
}

interface ResetPasswordForm {
  email: string
}

const { withMessage } = helpers
const { t } = useI18n()

const initialState = {
  email: '',
}

const state = reactive<ResetPasswordForm>({
  ...initialState,
})

const rules = {
  email: {
    required,
    emailField: withMessage(
      i18n.global.t('validations.emailField'),
      emailField
    ),
  },
}

const v$ = useVuelidate(rules, state)
const store = useAuthStore()

const isValid = computed(() => !v$.value.$invalid)
const isLoading = shallowRef(false)
const formErrors = ref<FormError[]>([])

function clear() {
  v$.value.$reset

  Object.entries(initialState).forEach(([key, value]) => {
    state[key as keyof ResetPasswordForm] = value
  })

  formErrors.value = []
}

const sendPasswordResetRequest = async () => {
  try {
    if (isLoading.value) return

    v$.value.$validate

    if (v$.value.$invalid) return

    isLoading.value = true

    await axios.post('/api/v1/users/reset_password/', { email: state.email })

    toast.success(t('toasts.sendPasswordResetRequest'))

    store.authMode = 'login'
  } catch (error) {
    console.log(error)

    if (axios.isAxiosError(error)) {
      const data = error.response?.data

      if (data && isObjectLike(data)) {
        const _formErrors = data['non_field_errors']
        if (Array.isArray(_formErrors)) {
          formErrors.value = (_formErrors as []).map((e) => ({
            title: e,
          }))
        }
      }
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <v-form @keydown.enter="sendPasswordResetRequest">
    <v-card>
      <v-text-field
        v-model="state.email"
        :error-messages="v$.email.$errors.map((e) => e.$message) as string[]"
        required
        @blur="v$.email.$touch"
        @input="v$.email.$touch"
        :disabled="isLoading"
        prepend-inner-icon="$iUser"
        :label="t('labels.email')"
        variant="outlined"
        class="my-2"
        autocomplete="email"
        color="info"
      />

      <v-card-text class="d-flex justify-end align-center">
        <v-btn
          :text="t('buttons.login')"
          variant="plain"
          color="info"
          class="text-capitalize"
          @click="store.authMode = 'login'"
        />
      </v-card-text>

      <v-card class="mb-12" color="surface-variant" variant="tonal">
        <v-card-text class="text-medium-emphasis text-caption">
          {{ t('auth.passwordReset.emailAsking') }}
        </v-card-text>
      </v-card>

      <v-card-item v-if="Object.values(formErrors).length">
        <v-alert color="error" variant="tonal" icon="$iAlert" slim>
          <v-list
            :items="formErrors"
            style="color: inherit; background-color: inherit"
            density="compact"
          />
        </v-alert>
      </v-card-item>

      <v-btn
        :text="t('buttons.sendPasswordResetRequest')"
        :disabled="!isValid"
        :loading="isLoading"
        @click="sendPasswordResetRequest"
        @keydown.enter=""
        block
        color="info"
        variant="tonal"
        class="mb-4"
      />
    </v-card>
  </v-form>
</template>
