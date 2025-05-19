<script setup lang="ts">
// Components
import GoogleIcon from '@/components/icons/GoogleIcon.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { useVuelidate } from '@vuelidate/core'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, reactive, ref, shallowRef } from 'vue'
import axios from 'axios'
import { helpers, sameAs } from '@vuelidate/validators'
import { required, minLength } from '@/common/vuelidate/validators'
import { isObjectLike } from 'lodash'
import {i18n} from "@/i18n/i18n";

interface FormError {
  title: string
}

interface RegistrationForm {
  username: string
  password: string
  passwordConfirmation: string
}

const { withAsync, withMessage } = helpers
const { t } = useI18n()

const initialState = {
  username: '',
  password: '',
  passwordConfirmation: '',
}

const usernameUniqueValidator = createUniqueValidator(
  '/api/v1/invest/validate_username/'
)

const state = reactive<RegistrationForm>({
  ...initialState,
})

const rules = {
  username: {
    required,
    minLengthValue: minLength(8),
    unique: withMessage(
      i18n.global.t('validations.usernameYetTaken'),
      withAsync(usernameUniqueValidator)
    ),
  },
  password: { required, minLengthValue: minLength(8) },
  passwordConfirmation: {
    required,
    sameAsRef: withMessage(
      () => i18n.global.t('validations.passwordMismatch'),
      sameAs(computed(() => state.password))
    ),
  },
}

const v$ = useVuelidate(rules, state)
const store = useAuthStore()

const isValid = computed(() => !v$.value.$invalid)
const isLoadig = shallowRef(false)
const passwordIsHidden = shallowRef(true)
const formErrors = ref<FormError[]>([])

function clear() {
  v$.value.$reset

  Object.entries(initialState).forEach(([key, value]) => {
    state[key as keyof RegistrationForm] = value
  })

  formErrors.value = []
}

function createUniqueValidator(endpoint: string) {
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  let abortController: AbortController | null = null

  return async (value: string) => {
    if (value.length < 8) return true

    if (timeoutId) clearTimeout(timeoutId)
    if (abortController) abortController.abort()

    return new Promise<boolean>((resolve) => {
      timeoutId = setTimeout(async () => {
        try {
          abortController = new AbortController()

          const response = await axios.get(endpoint, {
            params: { username: value },
            signal: abortController?.signal,
          })

          resolve(!response.data.isTaken)
        } catch (error) {
          if (axios.isCancel(error)) {
            resolve(false)
          } else {
            console.error('Validation error:', error)
            resolve(true)
          }
        }
      }, 500)
    })
  }
}

async function register() {
  if (isLoadig.value) return

  v$.value.$validate

  if (v$.value.$invalid) return

  const formData = new FormData()

  Object.entries({
    username: state.username,
    password: state.password,
  }).forEach(([key, value]) => {
    formData.append(key, value)
  })

  try {
    isLoadig.value = true

    await axios.post('/api/v1/users/', formData)

    const response = await axios.post('/api/v1/token/login/', formData)

    const token = response.data.auth_token
    store.token = token
    axios.defaults.headers.common['Authorization'] = `Token ${token}`

    localStorage.setItem('token', token)

    clear()
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
    isLoadig.value = false
  }
}
</script>

<template>
  <v-form @keydown.enter="register">
    <v-card>
      <v-text-field
        v-model="state.username"
        :error-messages="v$.username.$errors.map((e) => e.$message) as string[]"
        required
        @blur="v$.username.$touch"
        @input="v$.username.$touch"
        :disabled="isLoadig"
        prepend-inner-icon="$iUser"
        :label="t('labels.username')"
        variant="outlined"
        class="my-2"
        autocomplete="username"
        color="info"
      />
      <v-text-field
        v-model="state.password"
        :error-messages="v$.password.$errors.map((e) => e.$message) as string[]"
        required
        @blur="v$.password.$touch"
        @input="v$.password.$touch"
        :disabled="isLoadig"
        prepend-inner-icon="$iLock"
        :label="t('labels.password')"
        variant="outlined"
        class="my-2"
        autocomplete="new-password"
        color="info"
        :append-inner-icon="passwordIsHidden ? '$iEye' : '$iEyeOff'"
        @click:append-inner="passwordIsHidden = !passwordIsHidden"
        :type="passwordIsHidden ? 'password' : 'text'"
      />
      <v-text-field
        v-model="state.passwordConfirmation"
        :error-messages="
          v$.passwordConfirmation.$errors.map((e) => e.$message) as string[]
        "
        required
        @blur="v$.passwordConfirmation.$touch"
        @input="v$.passwordConfirmation.$touch"
        :disabled="isLoadig"
        prepend-inner-icon="$iLock"
        :label="t('labels.passwordConfirmation')"
        variant="outlined"
        class="my-2"
        autocomplete="new-password"
        color="info"
        :append-inner-icon="passwordIsHidden ? '$iEye' : '$iEyeOff'"
        @click:append-inner="passwordIsHidden = !passwordIsHidden"
        :type="passwordIsHidden ? 'password' : 'text'"
      />

      <v-card-item v-if="Object.values(formErrors).length">
        <v-alert color="error" variant="tonal" icon="$iAlert" slim closable>
          <v-list
            :items="formErrors"
            style="color: inherit; background-color: inherit"
            density="compact"
          />
        </v-alert>
      </v-card-item>

      <v-btn
        :text="t('buttons.registration')"
        :disabled="!isValid"
        :loading="isLoadig"
        @click="register"
        @keydown.enter=""
        block
        color="info"
        variant="tonal"
        class="mb-4"
      />
      <v-divider>{{ t('common.or') }}</v-divider>

      <v-card-actions class="justify-center">
        <v-btn variant="tonal">
          <v-icon>
            <google-icon />
          </v-icon>
        </v-btn>
        <v-btn variant="tonal">
          <v-icon>
            <google-icon />
          </v-icon>
        </v-btn>
        <v-btn variant="tonal">
          <v-icon>
            <google-icon />
          </v-icon>
        </v-btn>
      </v-card-actions>

      <v-card-text class="d-flex justify-center align-center">
        <span style="line-height: 1.5; margin-bottom: -1px">
          {{ t('auth.haveYetAccount') }}
        </span>
        <v-btn
          :text="t('buttons.login')"
          class="text-capitalize"
          variant="plain"
          slim
          color="info"
          @click="store.hasAccount = true"
        />
      </v-card-text>

      <v-card-text class="d-flex justify-center text-medium-emphasis">
        <span v-html="t('auth.disclaimer')" />
      </v-card-text>
    </v-card>
  </v-form>
</template>
