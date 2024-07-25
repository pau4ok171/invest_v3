<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminCharField",
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
<div class="admin-char-fieldset">
  <div class="admin-char-field">
    <input
        :required="isRequired"
        :disabled="isDisabled"
        :value="$attrs.modelValue"
        @input="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).value)"
        class="admin-char-field__input"
        placeholder=" "
    />
    <label class="admin-char-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
  </div>

  <div v-if="helpText" class="admin-char-field__help-text">{{ helpText }}</div>
</div>
</template>

<style scoped>

</style>