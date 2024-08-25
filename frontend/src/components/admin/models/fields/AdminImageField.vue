<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import UploadIcon from "@/components/icons/UploadIcon.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
import type {ErrorObject} from "@vuelidate/core";
import ResetIcon from "@/components/icons/ResetIcon.vue";

export default defineComponent({
  name: "AdminImageField",
  components: {ResetIcon, RoundedBlueButton, DeleteIcon, UploadIcon},
  data() {
    return {
      isDrugOver: false,
    }
  },
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
      type: Object as PropType<File>,
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
  methods: {
    uploadFile({currentTarget}: Event & { currentTarget: HTMLInputElement }) {
      if (currentTarget.files) {
        this.$emit('update:modelValue', currentTarget.files[0])
      }
      if (currentTarget.value) {
        currentTarget.value = ''
      }
      this.isDrugOver = false
    },
    getLogoURL() {
      try {
        return URL.createObjectURL(this.modelValue)
      } catch {
        return ''
      }
    },
    removeLogo() {
      if (this.modelValue?.size) {
        this.$emit('update:modelValue', {})
      }
    },
  },
})
</script>

<template>
<div class="admin-image-fieldset">
  <div class="admin-image-field">

    <button
      class="admin-image__reset-button"
      v-show="wasModified"
      @click="$emit('resetField')"
      v-tippy="{content: 'Click to reset field changes'}"
    >
      <ResetIcon/>
    </button>

    <div
        class="admin-image-field__input-box"
        :class="{'admin-image-field__input-box--drag': isDrugOver, 'admin-image-field__input-box--filled': modelValue?.size, 'admin-image-field__input-box--disabled': isDisabled}"
        @dragover="isDrugOver = true"
        @dragleave="isDrugOver = false"
    >

      <template v-if="!modelValue?.size">
        <input
            class="admin-image-field__input"
            id="admin-image-field"
            type="file"
            title=""
            accept="image/*"
            :required="isRequired"
            :disabled="isDisabled"
            @change="uploadFile"
        >
        <UploadIcon class="admin-image-field__icon"/>
      </template>

      <template v-else>
        <img class="admin-image-field__logo" :src="getLogoURL()" alt="logo">
        <RoundedBlueButton
            class="admin-image-field__remove-button"
            @click="removeLogo()"
            :disabled="isDisabled"
        >
          <DeleteIcon/>
        </RoundedBlueButton>
      </template>

    </div>

    <label class="admin-image-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
  </div>
  <div v-if="helpText" class="admin-image-field__help-text">{{ helpText }}</div>
  <div v-if="errors?.length" class="admin-image-field__errors">
    <div
        v-for="error in errors"
        :key="error.$uid"
        class="admin-image-field__error"
    >
      {{ error.$message }}
    </div>
  </div>
</div>
</template>

<style scoped lang="scss">
.admin-image-fieldset {
  margin: 16px 0;
  width: max-content;
  max-width: calc(280px + 18px + 18px);
  position: relative;
  padding: 2px 18px 0 0;
}
.admin-image-field {
  position: relative;
  line-height: 1.4rem;
  max-width: max-content;
  padding-right: 18px;
}
.admin-image-field__input {
  width: 100%;
  height: 100%;
  opacity: 0;
  position: absolute;
  z-index: 2;
  cursor: pointer;
}
.admin-image-field__input-box {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  outline: 2px dashed rgba(35, 148, 223, .5);
  outline-offset: -16px;

  width: 280px;
  height: 280px;
  padding: 10px 20px;

  border: 3px solid transparent;
  border-radius: 20px;
  background-image: linear-gradient(#1b222d, #1b222d), linear-gradient(315deg, #ee4297, #9176c6);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  overflow: hidden;

  font-size: 1.4rem;
  color: #fff;
  transition: outline .2s, width .5s, height .5s;

  &--drag {
    outline: 2px dashed rgba(35, 148, 223, 1);

    & > .admin-image-field__icon {
      fill: rgba(35, 148, 223, 1);
    }
  }

  &--filled {
    width: 166px;
    height: 166px;
    outline: none;
  }

  &--disabled {
    background: #1b222d;
    border-color: #92969c;
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
.admin-image-field__icon {
  width: 192px;
  height: 192px;
  fill: rgba(35, 148, 223, .5);
  margin-bottom: 20px;
  user-select: none;
  transition: outline .2s;
}
.admin-image-field__label {
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
.admin-image-field__help-text {
  color: #92969c;
  font-size: 1.2rem;
  padding-left: 20px;
  margin-top: 4px;
}
.admin-image-field__logo {
  width: 160px;
  height: 160px;
  background-color: white;
}
.admin-image-field__remove-button {
  position: absolute;
  top: 4px;
  right: 4px;
}
.admin-image-field__errors {
  width: max-content;
  margin: 10px 0 0 20px;
  border: 1px solid #c92432;
  border-radius: 8px;
  font-size: 1.2rem;
}
.admin-image-field__error {
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
.admin-image__reset-button {
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