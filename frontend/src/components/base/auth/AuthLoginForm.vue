<script setup lang="ts">
// Components
import SocialLogin from '@/components/base/auth/social/SocialLogin.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { useVuelidate } from '@vuelidate/core'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, reactive, ref, shallowRef } from 'vue'
import axios from 'axios'
import { isObjectLike } from 'lodash'

// Validators
import { required } from '@/common/vuelidate/validators'

interface FormError {
  title: string
}

interface LoginForm {
  username: string
  password: string
}

const initialState = {
  username: '',
  password: '',
}

const state = reactive<LoginForm>({
  ...initialState,
})

const rules = {
  username: { required },
  password: { required },
}

const v$ = useVuelidate(rules, state)
const store = useAuthStore()
const { t } = useI18n()

const isValid = computed(() => !v$.value.$invalid)
const isLoadig = shallowRef(false)
const passwordIsHidden = shallowRef(true)
const formErrors = ref<FormError[]>([])

function clear() {
  v$.value.$reset

  Object.entries(initialState).forEach(([key, value]) => {
    state[key as keyof LoginForm] = value
  })

  formErrors.value = []
}

async function login() {
  if (isLoadig.value) return

  v$.value.$validate

  if (v$.value.$invalid) return

  try {
    isLoadig.value = true

    await store.login(state.username, state.password)

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
  <v-form @keydown.enter="login">
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
        autocomplete="current-password"
        color="info"
        :append-inner-icon="passwordIsHidden ? '$iEye' : '$iEyeOff'"
        @click:append-inner="passwordIsHidden = !passwordIsHidden"
        :type="passwordIsHidden ? 'password' : 'text'"
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

      <v-card-actions class="justify-end">
        <v-btn
          :text="t('buttons.forgotPassword')"
          variant="plain"
          color="info"
          class="text-capitalize"
          @click="store.authMode = 'forgotPassword'"
        />
      </v-card-actions>
      <v-btn
        :text="t('buttons.login')"
        :disabled="!isValid"
        :loading="isLoadig"
        @click="login"
        @keydown.enter=""
        block
        color="info"
        variant="tonal"
        class="mb-4"
      />
      <v-divider>{{ t('common.or') }}</v-divider>

      <social-login />

      <v-card-text class="d-flex justify-center align-center">
        <span style="line-height: 1.5; margin-bottom: -1px">
          {{ t('auth.dontHaveAccount') }}
        </span>
        <v-btn
          :text="t('buttons.create')"
          class="text-capitalize"
          variant="plain"
          slim
          color="info"
          @click="store.authMode = 'registration'"
        />
      </v-card-text>
    </v-card>
  </v-form>
</template>
