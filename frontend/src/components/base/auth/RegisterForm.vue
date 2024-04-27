<template>
  <div class="form__fields">
    <AuthField>
      <AuthLabel for="username">Username</AuthLabel>
      <AuthInput
        :class="{'form__input--success': !checks.username.isError && checks.username.isInit, 'form__input--error': checks.username.isError && checks.username.isInit}"
        v-model:inputValue="formData.new_username"
        name="username"
        autocomplete="username"
      />
      <AuthHelpText
          :check="checks.username"
      />
    </AuthField>

    <AuthField>
      <AuthLabel for="password1">Password</AuthLabel>
      <AuthInput
        :class="{'form__input--success': !checks.password.isError && checks.password.isInit, 'form__input--error': checks.password.isError && checks.password.isInit}"
        v-model:inputValue="formData.new_password1"
        type="password"
        name="password1"
        autocomplete="new-password"
      />
      <AuthHelpText
        :check="checks.password"
      />
    </AuthField>

    <AuthField>
      <AuthLabel for="password2">Password confirmation</AuthLabel>
      <AuthInput
        :class="{'form__input--success': !checks.password.isError && checks.password.isInit, 'form__input--error': checks.password.isError && checks.password.isInit}"
        v-model:inputValue="formData.new_password2"
        type="password"
        name="password2"
        autocomplete="new-password"
      />
    </AuthField>
  </div>
</template>

<script lang="ts">
  import AuthField from "@/components/UI/auth/AuthField.vue";
  import AuthLabel from "@/components/UI/auth/AuthLabel.vue";
  import AuthInput from "@/components/UI/auth/AuthInput.vue";
  import axios from "axios";
  import AuthHelpText from "@/components/UI/auth/AuthHelpText.vue";

  export default {
    name: 'RegisterForm',
    components: {
      AuthHelpText,
      AuthInput,
      AuthLabel,
      AuthField
    },
    props: {
      formData: {
        type: Object,
        new_username: '',
        new_password1: '',
        new_password2: '',
      },
      formIsValid: Boolean,
    },
    data() {
      return {
        checks: {
          username: {
            isInit: false,
            isError: false,
            message: 'minimum 8 characters'
          },
          password: {
            isInit: false,
            isError: false,
            message: 'minimum 8 characters'
          },
        }
      }
    },
    watch: {
      formData: {
        async handler(obj) {
          const formData = JSON.parse(JSON.stringify(obj))
          const fieldList = {'new_username': '', 'new_password1': '', 'new_password2': ''}
          const formDataFields = {...fieldList, ...formData}

          let formIsValid = false

          // Проверить поле имя пользователя на заполненность
          if (formDataFields.new_username.length >= 8) {
            this.checks.username.isInit = true
            // Проверить имя пользователя на уникальность
            const formData = new FormData()
            Object.entries({
                username: formDataFields.new_username,
            }).forEach(([key, val]) => formData.append(key, val))

            await axios
              .post('/invest/api/v1/validate_username/', formData)
              .then(response => {
                this.checks.username.isError = response.data.isTaken
                this.checks.username.message = response.data.message
              })
              .catch(error => console.log(error))
          } else {
            this.checks.username.isInit = false
            this.checks.username.isError = false
            this.checks.username.message = 'minimum 8 characters'
          }

          // Проверить поле пароль на заполненность
          if (formDataFields.new_password1.length >= 8 && formDataFields.new_password2.length >= 8) {
            this.checks.password.isInit = true
            // Проверить на совпадение полей с паролем
            if (formDataFields.new_password1 === formDataFields.new_password2) {
              this.checks.password.isError = false
              this.checks.password.message = 'password match'
            } else {
              this.checks.password.isError = true
              this.checks.password.message = 'password doesn\'t match'
            }
          } else {
            this.checks.password.isInit = false
            this.checks.password.isError = false
            this.checks.password.message = 'minimum 8 characters'
          }

          // Проверить на заполненность
          if (
              (this.checks.username.isInit && !this.checks.username.isError)
              &&
              (this.checks.password.isInit && !this.checks.password.isError)
          ) {
            formIsValid = true
          }
          if (this.formIsValid !== formIsValid) {
            this.$emit('setFormIsValid', formIsValid)
          }
        },
        deep: true
      }
    },
  }
</script>

