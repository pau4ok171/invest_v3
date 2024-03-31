<template>
  <BaseInput
    type="text"
    class="form__input"
    maxlength="255"
    :inputValue
    @updateInput="updateInput"
  />
</template>

<script lang="ts">
 import BaseInput from "@/components/UI/base/BaseInput.vue";

 export default {
   name: 'AuthInput',
   components: {BaseInput},
   props: {
     inputValue: [String, Number],
   },
   methods: {
     updateInput(value) {
       this.$emit('update:inputValue', value)
     },
   },
 }
</script>

<style scoped>
  .form__input {
    padding: 14px 48px 14px 12px;
    font-size: 1.4rem;
    width: 100%;
    border-radius: 4px;
    height: 40px;
    color: rgb(38, 46, 58);
    border: 1px solid rgb(38, 46, 58, .2);
    background-color: rgba(38, 46, 58, .05);
    transition: border .2s ease 0s, background-color .2s ease 0s;
    caret-color: rgb(35, 148, 223);
  }
  .form__input::placeholder {
    color: rgba(38, 46, 58, .5);
  }
  .form__input:hover,
  .form__input:focus {
    border-color: #000;
    transition: border-color .5s ease;
  }
  .form__input--success {
    border: 2px solid var(--color-success);
  }
  .form__input--error {
    border: 2px solid var(--color-error);
  }
  .form__input--success:hover,
  .form__input--success:focus {
    border-color: var(--color-success);
  }
  .form__input--error:hover,
  .form__input--error:focus {
    border-color: var(--color-error);
  }
</style>