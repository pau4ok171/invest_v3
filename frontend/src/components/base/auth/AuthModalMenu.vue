<template>
  <ModalMenu @closeModalMenu="closeModalMenu">
    <div class="auth-form">
      <h1 class="auth-form__title">Finargo</h1>
      <h2 class="auth-form__subtitle">Your best invest analysis provider</h2>

      <AuthForm
          @submitForm="submitForm"
          :registerIsChosen
          :errors
          v-model:formData="formData"
          v-model:formIsValid="formIsValid"
      />

      <SocialAuthForm/>

      <div class="auth-form__change-form">
        <template v-if="!registerIsChosen">Еще нет аккаунта? <span @click="changeForm">Создать</span></template>
        <template v-else>Уже есть аккаунт? <span @click="changeForm">Войти</span></template>
      </div>

      <div class="auth-form__conditions">
          By using Simply Wall St you are agreeing to our <br>
          <a href="#" target="_blank">terms and conditions</a>.
          Simply Wall St provides <br>general investment advice only.
      </div>
    </div>
  </ModalMenu>
</template>

<script lang="ts">
  import ModalMenu from "@/components/UI/ModalMenu.vue";
  import SocialAuthForm from "@/components/base/auth/SocialAuthForm.vue";
  import AuthForm from "@/components/base/auth/AuthForm.vue";
  import store from "@/store";
  import axios from "axios";
  import Loader from "@/components/UI/Loader.vue";

  export default {
    name: 'AuthModalMenu',
    components: {
      Loader,
      AuthForm,
      SocialAuthForm,
      ModalMenu,
    },
    data() {
      return {
        registerIsChosen: false,
        errors: [],
        formData: {},
        formIsValid: false,
      }
    },
    methods: {
      closeModalMenu() {
        store.commit('setAuthModalMenuIsActive', false)
        this.formData = {}
        this.errors = []
        this.formIsValid = false
        this.registerIsChosen = false
      },
      changeForm() {
        this.formData = {}
        this.errors = []
        this.formIsValid = false
        this.registerIsChosen = !this.registerIsChosen
      },
      async submitForm() {
        let formData
        this.errors = []

        if (this.registerIsChosen) {
          store.commit('setIsLoading', true)

          // TODO: Проверить на ошибки|На уникальность логина
          formData = {
            username: this.formData.new_username,
            password: this.formData.new_password1,
          }
          await axios
            .post('/api/v1/users/', formData)
            .then(response => {})
            .catch(this.catchError)

          store.commit('setIsLoading', false)

        } else {
          formData = {
            username: this.formData.current_username,
            password: this.formData.current_password,
          }
        }
        if (!this.errors.length) {
          await this.loginUser(formData)
        }

    },
    async loginUser(formData) {
      store.commit('setIsLoading', true)
      await axios
        .post('/api/v1/token/login/', formData)
        .then(response => {
          const token = response.data.auth_token

          store.commit('setToken', token)

          axios.defaults.headers.common["Authorization"] = `Token ${token}`

          localStorage.setItem("token", token)

          // Закрыть AuthModalMenu
          this.closeModalMenu()
        })
        .catch(this.catchError)
      store.commit('setIsLoading', false)
    },
    catchError(error) {
      if (error.response) {
        for (const property in error.response.data) {
          this.errors.push(`${property}: ${error.response.data[property]}`)
        }

        console.log(JSON.stringify(error.response.data))

      } else if (error.message) {
        this.errors.push('Something went wrong. Please try again')

        console.log(JSON.stringify(error))
      }
    },
  },
}
</script>

<style scoped>
  .auth-form {
    padding: 36px;
  }
  .auth-form__title {
    font-size: 2.2rem;
    text-align: center;
    margin-top: 14px;
  }
  .auth-form__subtitle {
    text-align: center;
    opacity: .5;
    margin-top: 14px;
  }
  .auth-form__conditions {
    font-size: 1.2em;
    line-height: 1.5;
    text-align: center;
    color: rgb(95, 104, 117);
    margin: 0;
  }
  .auth-form__conditions a {
    border-bottom: 1px solid rgba(38, 46, 58, .3);
    transition: border-bottom .2s ease;
  }
  .auth-form__conditions a:hover {
    border-bottom: 1px solid rgba(38, 46, 58, .6);
  }
    .auth-form__change-form {
    margin: 16px 0;
    text-align: center;
    font-size: 1.6rem;
    line-height: 1.7;
    color: #000;
  }
  .auth-form__change-form span {
    color: var(--blue);
    font-weight: 500;
    border-bottom: 1px solid rgba(35, 148, 223, 0);
    transition: border-bottom .2s ease;
    cursor: pointer;
  }
  .auth-form__change-form span:hover {
    border-bottom: 1px solid rgba(35, 148, 223, 1);
  }
</style>