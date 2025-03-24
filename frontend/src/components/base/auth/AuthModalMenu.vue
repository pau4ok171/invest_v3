<script lang="ts">
import SocialAuthForm from '@/components/base/auth/SocialAuthForm.vue'
import AuthForm from '@/components/base/auth/AuthForm.vue'
import axios, { AxiosError } from 'axios'
import Loader from '@/components/UI/Loader.vue'
import { defineComponent } from 'vue'
import { useAuthStore } from '@/store/auth'

export default defineComponent({
  name: 'AuthModalMenu',
  components: {
    Loader,
    AuthForm,
    SocialAuthForm,
  },
  setup: () => ({ authStore: useAuthStore() }),
  data() {
    return {
      registerIsChosen: false,
      errors: [] as Array<String>,
      formData: {
        new_username: '',
        new_password1: '',
        current_username: '',
        current_password: '',
      },
      EMPTY_FORM_DATA: {
        new_username: '',
        new_password1: '',
        current_username: '',
        current_password: '',
      },
      formIsValid: false,
    }
  },
  unmounted() {
    this.cleanModalMenu()
  },
  methods: {
    cleanModalMenu() {
      this.formData = this.EMPTY_FORM_DATA
      this.errors = []
      this.formIsValid = false
      this.registerIsChosen = false
    },
    changeForm() {
      this.formData = this.EMPTY_FORM_DATA
      this.errors = []
      this.formIsValid = false
      this.registerIsChosen = !this.registerIsChosen
    },
    async submitForm() {
      const formData = new FormData()
      this.errors = []
      if (this.registerIsChosen) {
        // this.setIsLoading(true)

        // TODO: Проверить на ошибки|На уникальность логина

        Object.entries({
          username: this.formData.new_username,
          password: this.formData.new_password1,
        }).forEach(([key, val]) => formData.append(key, val))

        await axios
          .post('/api/v1/users/', formData)
          .then(() => {})
          .catch(this.catchError)

        // this.setIsLoading(false)
      } else {
        Object.entries({
          username: this.formData.current_username,
          password: this.formData.current_password,
        }).forEach(([key, val]) => formData.append(key, val))
      }
      if (!this.errors.length) {
        await this.loginUser(formData)
      }
    },
    async loginUser(formData: FormData) {
      // this.setIsLoading(true)
      await axios
        .post('/api/v1/token/login/', formData)
        .then((response) => {
          const token = response.data.auth_token

          this.authStore.token = token

          axios.defaults.headers.common['Authorization'] = `Token ${token}`

          localStorage.setItem('token', token)

          this.cleanModalMenu()

          document.location.reload()
        })
        .catch(this.catchError)
      // this.setIsLoading(false)
    },
    catchError(error: AxiosError) {
      if (error.response) {
        const error_data = error.response.data as Array<String>
        for (const property in error_data) {
          this.errors.push(`${property}: ${error_data[property]}`)
        }
        console.log(JSON.stringify(error.response.data))
      } else if (error.message) {
        this.errors.push('Something went wrong. Please try again')
        console.log(JSON.stringify(error))
      }
    },
  },
})
</script>

<template>
  <div class="auth-form">
    <AuthForm
      @submitForm="submitForm"
      :registerIsChosen
      :errors
      v-model:formData="formData"
      v-model:formIsValid="formIsValid"
    />

    <SocialAuthForm />

    <div class="auth-form__change-form">
      <template v-if="!registerIsChosen"
        >Еще нет аккаунта? <span @click="changeForm">Создать</span></template
      >
      <template v-else
        >Уже есть аккаунт? <span @click="changeForm">Войти</span></template
      >
    </div>

    <div class="auth-form__conditions">
      By using Simply Wall St you are agreeing to our <br />
      <a href="#" target="_blank">terms and conditions</a>. Simply Wall St
      provides <br />general investment advice only.
    </div>
  </div>
</template>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  padding-inline: 24px;
}
.auth-form__conditions {
  line-height: 1.5;
  text-align: center;
  color: rgb(95, 104, 117);
  margin: 0;
}
.auth-form__conditions a {
  border-bottom: 1px solid rgba(38, 46, 58, 0.3);
  transition: border-bottom 0.2s ease;
}
.auth-form__conditions a:hover {
  border-bottom: 1px solid rgba(38, 46, 58, 0.6);
}
.auth-form__change-form {
  margin: 16px 0;
  text-align: center;
  line-height: 1.7;
  color: #000;
}
.auth-form__change-form span {
  color: var(--blue);
  font-weight: 500;
  border-bottom: 1px solid rgba(35, 148, 223, 0);
  transition: border-bottom 0.2s ease;
  cursor: pointer;
}
.auth-form__change-form span:hover {
  border-bottom: 1px solid rgba(35, 148, 223, 1);
}
</style>
