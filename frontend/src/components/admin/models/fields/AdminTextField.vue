<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from "vue";
import type {ErrorObject} from "@vuelidate/core";
import ResetIcon from "@/components/icons/ResetIcon.vue";

export default defineComponent({
  name: "AdminTextField",
  components: {ResetIcon},
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
    errors: {
      type: Object as PropType<ErrorObject[]>,
    },
    wasModified: {
      type: Boolean,
      default: false,
    },
  },
})
</script>

<template>
<div class="admin-text-fieldset">

  <button
    class="admin-text__reset-button"
    v-show="wasModified"
    @click="$emit('resetField')"
    v-tippy="{content: 'Click to reset field changes'}"
  >
    <ResetIcon/>
  </button>

  <div class="admin-text-field">
    <div class="admin-text-field__tab"></div>
    <textarea
        :required="isRequired"
        :disabled="isDisabled"
        @input="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).value)"
        @blur="$emit('blur')"
        :value="modelValue"
        class="admin-text-field__textarea"
        cols="50"
        rows="15"
        placeholder=" "
    />
    <label class="admin-text-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
  </div>

  <div v-if="helpText" class="admin-text-field__help-text">{{ helpText }}</div>
  <div v-if="errors?.length" class="admin-text-field__errors">
    <div
        v-for="error in errors"
        :key="error.$uid"
        class="admin-text-field__error"
    >
      {{ error.$message }}
    </div>
  </div>
</div>
</template>

<style scoped>
.admin-text-fieldset {
  position: relative;
  width: max-content;
  margin: 16px 0;
  padding: 2px 18px 0 0;
}
.admin-text-field {
  position: relative;
  display: inline-block;
  line-height: 1.4rem;
}
.admin-text-field:after {
    content: "";
    border-top: 2px solid #555;
    width: 16px;
    transform: rotate(-45deg);
    background: transparent;
    position: absolute;
    right: 4px;
    bottom: 16px;
    pointer-events: none;
    border-radius: 25%;
}
.admin-text-field__textarea {
  position: relative;
  min-height: 200px;
  max-height: 800px;
  min-width: 600px;
  max-width: 800px;
  font-size: 1.4rem;
  scroll-padding: 50px 0 50px 0;
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
.admin-text-field__textarea::-webkit-scrollbar {
  width: 10px;
}
.admin-text-field__textarea::-webkit-scrollbar-track {
  -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
  background-color: #f9f9fd;
  border-radius: 10px;
  margin: 15px 0 25px;
}
.admin-text-field__textarea::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: linear-gradient(180deg, #00c6fb, #005bea);
}
.admin-text-field__textarea::-webkit-resizer {
  display: none;
}
/* White square */
.admin-text-field__textarea::-webkit-scrollbar-corner {
  display: none;
}
.admin-text-field__tab {
  border-top: 2px solid #555;
  width:10px;
  transform: rotate(-45deg);
  position: absolute;
  bottom: 12px;
  right: 4px;
  z-index: 1;
  pointer-events: none;
  border-radius:25%;
}
.admin-text-field__label {
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
.admin-text-field__help-text {
  color: #92969c;
  font-size: 1.2rem;
  padding-left: 20px;
  margin-top: 4px;
}
.admin-text-field__errors {
  width: max-content;
  margin: 10px 0 0 20px;
  border: 1px solid #c92432;
  border-radius: 8px;
  font-size: 1.2rem;
}
.admin-text-field__error {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px;
  color: #c92432;

  &::before {
    content: '';
    display: inline-block;
    margin-right: 1px;
    width: 5px;
    height: 5px;
    background-color: #c92432;
    border-radius: 2.5px;
  }
}
.admin-text__reset-button {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 0;
  right: 0;
  border: 1px solid transparent;
  border-radius: 4px;
  background-color: rgba(53, 110, 233, .1);
  transition: background-color .4s;
  cursor: pointer;

  &:hover {
    background-color: rgba(53, 110, 233, .2);
  }

  & svg {
    fill: var(--blue);
    width: 16px;
    height: 16px;
    user-select: none;
  }
}
</style>