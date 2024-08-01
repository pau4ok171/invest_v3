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
<div class="admin-image-field">
  <input
      type="file"
      accept="image/*"
      :required="isRequired"
      :disabled="isDisabled"
      @change="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).files[0])"
  >
</div>
</template>

<style scoped>

</style>