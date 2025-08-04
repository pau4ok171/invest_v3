<script setup lang="ts">
// Components
import SocialLogin from "@/components/base/auth/social/SocialLogin.vue";

// Composables
import { useAuthStore } from '@/store/auth'
import { useVuelidate } from '@vuelidate/core'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, reactive, ref, shallowRef } from 'vue'
import axios from 'axios'
import { i18n } from '@/i18n/i18n'
import { isObjectLike } from 'lodash'

// Validators
import { helpers, sameAs } from '@vuelidate/validators'
import { required, minLength, emailField } from '@/common/vuelidate/validators'

interface FormError {
  title: string
}

interface RegistrationForm {
  username: string
  password: string
  passwordConfirmation: string
  email: string
}

const { withAsync, withMessage } = helpers
const { t } = useI18n()

const initialState = {
  username: '',
  password: '',
  passwordConfirmation: '',
  email: '',
}

const usernameUniqueValidator = createUniqueValidator(
  '/api/v1/invest/validate-username/'
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
  email: {
    required,
    emailField: withMessage(
      i18n.global.t('validations.emailField'),
      emailField
    ),
  },
}

const v$ = useVuelidate(rules, state)
const authStore = useAuthStore()

const isValid = computed(() => !v$.value.$invalid)
const isLoading = shallowRef(false)
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
  if (isLoading.value) return

  v$.value.$validate

  if (v$.value.$invalid) return

  const formData = new FormData()

  Object.entries({
    username: state.username,
    password1: state.password,
    password2: state.passwordConfirmation,
    email: state.email,
  }).forEach(([key, value]) => {
    formData.append(key, value)
  })

  try {
    isLoading.value = true

    await axios.post('/api/v1/auth/registration/', formData)

    authStore.registrationEmail = (formData.get('email') as string) || ''
    authStore.authMode = 'emailConfirmation'

    clear()
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const data = error.response?.data
      console.log(error)

      if (data && isObjectLike(data)) {
        formErrors.value = (Object.values(data).flat() as string[]).map(e => ({title: e}))
      }
    }
  } finally {
    isLoading.value = false
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
        :disabled="isLoading"
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
        :disabled="isLoading"
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
        :disabled="isLoading"
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

      <v-text-field
        v-model="state.email"
        :error-messages="v$.email.$errors.map((e) => e.$message) as string[]"
        required
        @blur="v$.email.$touch"
        @input="v$.email.$touch"
        prepend-inner-icon="$iLock"
        :label="t('labels.email')"
        variant="outlined"
        class="my-2"
        autocomplete="email"
        color="info"
      />

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
        :text="t('buttons.registration')"
        :disabled="!isValid"
        :loading="isLoading"
        @click="register"
        @keydown.enter=""
        block
        color="info"
        variant="tonal"
        class="mb-4"
      />
      <v-divider>{{ t('common.or') }}</v-divider>

      <social-login/>

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
          @click="authStore.authMode = 'login'"
        />
      </v-card-text>

      <v-card-text
        class="d-flex justify-center text-center text-medium-emphasis"
      >
        <span>{{ t('auth.disclaimer.prefix') }}<a href="#" target="_blank">{{ t('auth.disclaimer.terms') }}</a>{{ t('auth.disclaimer.suffix') }}</span>
      </v-card-text>
    </v-card>
  </v-form>
</template>
