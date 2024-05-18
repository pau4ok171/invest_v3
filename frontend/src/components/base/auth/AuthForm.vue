<script lang="ts">
import AuthButton from "@/components/UI/auth/AuthButton.vue";
import AuthLabel from "@/components/UI/auth/AuthLabel.vue";
import AuthInput from "@/components/UI/auth/AuthInput.vue";
import AuthField from "@/components/UI/auth/AuthField.vue";
import LoginForm from "@/components/base/auth/LoginForm.vue";
import RegisterForm from "@/components/base/auth/RegisterForm.vue";
import {defineComponent} from "vue";
import type {PropType} from "vue";
import type {loginAuthData, registerAuthData} from "@/types/auth";

export default defineComponent({
  name: 'AuthForm',
  props: {
    registerIsChosen: {
      type: Boolean,
      required: true
    },
    errors: {
      type: Array<String>,
      required: true,
    },
    formData: {
      type: Object as PropType<loginAuthData|registerAuthData>,
      required: true,
    },
    formIsValid: Boolean,
  },
  components: {
    RegisterForm,
    LoginForm,
    AuthField,
    AuthInput,
    AuthLabel,
    AuthButton
  },
  methods: {
    setFormIsValid(formIsValid: Boolean) {
      this.$emit('update:formIsValid', formIsValid)
    },
  },
})
</script>

<template>
<form @submit.prevent="$emit('submitForm')" class="form">

  <LoginForm
      v-if="!registerIsChosen"
      :formData
      :formIsValid
      @setFormIsValid="setFormIsValid"
  />
  <RegisterForm
      v-else
      :formData
      :formIsValid
      @setFormIsValid="setFormIsValid"
  />

  <div class="form__errors" v-if="errors.length">
    <p v-for="error in errors">{{ error }}</p>
  </div>

  <div class="form__forgot-password" v-if="!registerIsChosen">
      <a href="#">Забыли пароль?</a>
  </div>

  <AuthButton :disabled="!formIsValid">
    <template v-if="!registerIsChosen">Войти</template>
    <template v-else>Регистрация</template>
  </AuthButton>

</form>
</template>

<style scoped>
.form {
  margin-top: 25px;
  min-height: 238px;
}
.form__forgot-password {
  font-size: 1.2rem;
  line-height: 1.5;
  margin-top: 8px;
  text-align: right;
  text-decoration: underline;
  color: rgb(35, 148, 223);
}
.form__errors {
  font-size: 1.2rem;
  padding: 12px;
  margin-bottom: 16px;
  background-color: var(--color-error);
}
</style>