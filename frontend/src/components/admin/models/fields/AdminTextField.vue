<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminTextField",
  props: {
    label: {
      type: String,
      default: 'Label',
    },
    helpText: {
      type: String
    },
    isRequired: {
      type: Boolean,
      default: false,
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
  },
})
</script>

<template>
<div class="admin-text-fieldset">
  <div class="admin-text-field">
    <div class="admin-text-field__tab"></div>
    <textarea
        :required="isRequired"
        :disabled="isDisabled"
        @input="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).value)"
        :value="($attrs.modelValue as any)"
        class="admin-text-field__textarea"
        cols="50"
        rows="15"
        placeholder=" "
    />
    <label class="admin-text-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
  </div>

  <div v-if="helpText" class="admin-text-field__help-text">{{ helpText }}</div>
</div>
</template>

<style scoped>

</style>