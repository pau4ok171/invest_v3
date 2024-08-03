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
    modelValue: {
      type: String,
      default: '',
      required: true,
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
        :value="modelValue"
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
.admin-char-fieldset {
  margin: 16px 0;
}
.admin-char-field {
  position: relative;
  line-height: 1.4rem;
}
.admin-char-field__input {
  position: relative;
  width: 400px;
  font-size: 1.4rem;
  color: #fff;
  outline: none;
  padding: 10px 20px;
  border: 3px solid transparent;
  border-radius: 20px;
  background-image: linear-gradient(#1b222d, #1b222d), linear-gradient(315deg, #ee4297, #9176c6);
  background-origin: border-box;
  background-clip: padding-box, border-box;

  &:disabled {
    background: #1b222d;
    border-color: #92969c;
  }
  &:placeholder-shown + label {
    transform: translateY(0);
  }
  &:focus {
    border-color: #2b96f1;
            box-shadow: inset 1px 2px 4px 0 rgb(179 30 30 / 10%), 3px 5px 12px 2px rgb(43 150 241 / 40%);

    & + label {
      color: #2b96f1;
      transform: translateY(-20px);
    }
  }
}
.admin-char-field__label {
  color: #fff;
  border-radius: 20px;
  font-size: 1.4rem;
  text-transform: uppercase;
  position: absolute;
  z-index: 2;
  left: 20px;
  top: 14px;
  padding: 0 5px;
  pointer-events: none;
  background: #1b222d;
  transition: transform .1s ease;
  transform: translateY(-20px);
}
.admin-char-field__help-text {
  color: #92969c;
  font-size: 1.2rem;
  padding-left: 20px;
  margin-top: 4px;
}
</style>