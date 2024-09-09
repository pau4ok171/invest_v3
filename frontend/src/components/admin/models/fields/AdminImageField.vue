<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import UploadIcon from "@/components/icons/UploadIcon.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";

export default defineComponent({
  name: "AdminImageField",
  components: {
    RoundedBlueButton,
    DeleteIcon,
    UploadIcon
  },
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
    fieldStatus: {
      type: String,
      required: true,
    },
  },
  methods: {
    uploadFile({currentTarget}: Event & { currentTarget: HTMLInputElement }) {
      if (currentTarget.files) {
        this.$emit('update:modelValue', currentTarget.files[0])
        this.$emit('touch')
        this.$emit('commitValidator')
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
        this.$emit('touch')
      }
    },
  },
})
</script>

<template>
<div
    class="admin-image-field"
    :class="{'admin-image-field--valid': fieldStatus === 'valid', 'admin-image-field--invalid': fieldStatus === 'invalid'}"
>
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
</template>

<style scoped lang="scss">
.admin-image-field {
  position: relative;
  line-height: 1.4rem;
  max-width: max-content;
  padding-right: 18px;
  &--valid .admin-image-field__input-box {
    background-image: linear-gradient(var(--admin-field-default-backgroud-color), var(--admin-field-default-backgroud-color)), linear-gradient(315deg, var(--admin-field-success-gradient-color-start), var(--admin-field-success-gradient-color-finish));
  }
  &--invalid .admin-image-field__input-box {
    background-image: linear-gradient(var(--admin-field-default-backgroud-color), var(--admin-field-default-backgroud-color)), linear-gradient(315deg, var(--admin-field-error-gradient-color-start), var(--admin-field-error-gradient-color-finish));
  }
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
</style>