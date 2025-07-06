<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'
import { useAuthStore } from '@/store/auth'
import { useVuelidate } from '@vuelidate/core'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, reactive, ref, shallowRef, onMounted } from 'vue'
import { isObjectLike } from 'lodash'
import { toast } from 'vue3-toastify'
import { i18n } from '@/i18n/i18n'
import axios from 'axios'

// Validators
import { helpers, sameAs } from '@vuelidate/validators'
import { minLength, required } from '@/common/vuelidate/validators'

const props = defineProps<{
  uid: string
  token: string
}>()

interface FormError {
  title: string
}

interface PasswordResetForm {
  password: string
  passwordConfirmation: string
}

const { withMessage } = helpers
const { t } = useI18n()

const initialState = {
  password: '',
  passwordConfirmation: '',
}

const state = reactive<PasswordResetForm>({
  ...initialState,
})

const rules = {
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
const pageStore = usePageStore()
const router = useRouter()

const isValid = computed(() => !v$.value.$invalid)
const isLoading = shallowRef(false)
const passwordIsHidden = shallowRef(true)
const formErrors = ref<FormError[]>([])

const resetPassword = async () => {
  try {
    if (isLoading.value) return

    v$.value.$validate

    if (v$.value.$invalid) return

    isLoading.value = true

    await axios.post(`/api/v1/auth/password/reset/confirm/`, {
      uid: props.uid,
      token: props.token,
      new_password1: state.password,
      new_password2: state.passwordConfirmation,
    })

    clear()

    toast.success(t('toasts.passwordResetSuccess'), {
      autoClose: 3000,
      onClose: () => router.push({ name: 'home' })
    })
  } catch (error) {
    console.log(error)

    toast.error(t('toasts.somethingWrong'))

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

function clear() {
  v$.value.$reset

  Object.entries(initialState).forEach(([key, value]) => {
    state[key as keyof PasswordResetForm] = value
  })

  formErrors.value = []
}

onMounted(() => {
  pageStore.loading = false
})
</script>

<template>
  <v-card width="500" max-height="min-content" location="center">
    <v-card-item>
      <v-form @keydown.enter="resetPassword">
        <v-alert :text="t('auth.passwordReset.resetInstruction')" />

        <v-text-field
          v-model="state.password"
          :error-messages="
            v$.password.$errors.map((e) => e.$message) as string[]
          "
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
          :text="t('buttons.resetPassword')"
          :disabled="!isValid"
          :loading="isLoading"
          @click="resetPassword"
          @keydown.enter=""
          block
          color="info"
          variant="tonal"
          class="mb-4"
        />
      </v-form>
    </v-card-item>
  </v-card>
</template>
