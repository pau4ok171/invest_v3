<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminImageField",
  components: {RoundedBlueButton, DeleteIcon, UploadIcon},
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
  },
})
</script>

<template>
<div class="admin-image-fieldset">
  <div class="admin-image-field">

    <div
        class="admin-image-field__input-box"
        :class="{'admin-image-field__input-box--drag': isDrugOver, 'admin-image-field__input-box--filled': modelValue.size}"
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
        >
          <DeleteIcon/>
        </RoundedBlueButton>
      </template>

    </div>

    <label class="admin-image-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
  </div>
  <div v-if="helpText" class="admin-image-field__help-text">{{ helpText }}</div>
</div>
</template>

<style scoped>

</style>