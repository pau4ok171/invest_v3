<script lang="ts">
  import AuthLabel from "@/components/UI/auth/AuthLabel.vue";
  import AuthInput from "@/components/UI/auth/AuthInput.vue";
  import AuthField from "@/components/UI/auth/AuthField.vue";
  import {defineComponent} from "vue";
  import type {PropType} from "vue";
  import type {loginAuthData} from "@/types/auth";

  export default defineComponent({
    name: 'LoginForm',
    components: {AuthField, AuthInput, AuthLabel},
    props: {
      formData: {
        type: Object as PropType<loginAuthData>,
        required: true,
      },
      formIsValid: Boolean,
    },
    watch: {
      formData: {
        handler(obj) {
          const formData = JSON.parse(JSON.stringify(obj))
          const fieldList = {'current_username': formData.current_username, 'current_password': formData.current_password}

          let formIsValid = true

          for (let val of Object.values(fieldList)) {
            if (val) {
               if (val.trim() === '') {
                formIsValid = false
              }
            } else {
              formIsValid = false
            }
          }

          if (this.formIsValid !== formIsValid) {
            this.$emit('setFormIsValid', formIsValid)
          }
        },
        deep: true
      }
    },
  })
</script>

<template>
  <div class="form__fields">
    <AuthField>
      <AuthLabel  for="username">Username</AuthLabel>
      <AuthInput v-model:inputValue="formData.current_username" id="username" autocomplete="username"/>
    </AuthField>

    <AuthField>
      <AuthLabel for="password">Password</AuthLabel>
      <AuthInput v-model:inputValue="formData.current_password" type="password" id="password" autocomplete="current-password"/>
    </AuthField>
  </div>
</template>
