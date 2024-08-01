<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminModelForm",
  components: {
    RoundedDarkBlueButton,
    AdminImageField,
    AdminSelectorField,
    AdminCheckBoxField,
    AdminTextField,
    AdminCharField
  },
  data() {
    return {
      isVisible: false,
      companyName: '',
      ticker: '',
      slug: '',
      uid: '',
      country: {name: '', slug: ''} as SelectorOption,
      market: {name: '', slug: ''} as SelectorOption,
      sector: {name: '', slug: ''} as SelectorOption,
      industry: {name: '', slug: ''} as SelectorOption,
      logo: {} as File,
      description: '',
      isFund: false,
      city: '',
      website: '',
      founded: '',
    }
  },
  watch: {
    ticker(value) {
      this.slug = value.toLowerCase()
    },
  },
})
</script>

<template>

</template>

<style scoped>

</style>