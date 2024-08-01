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
<div class="admin-model__admin-model-form">
  <AdminCheckBoxField
      v-model="isVisible"
      label="Company is publicly visible"
  />
  <AdminCharField
      v-model="companyName"
      :is-required="true"
      label="Company Name"
  />
  <AdminCharField
      v-model="ticker"
      :is-required="true"
      label="Ticker"
  />
  <AdminCharField
      v-model="slug"
      :is-required="true"
      :is-disabled="true"
      label="Slug"
  />
  <AdminCharField
      v-model="uid"
      :is-required="true"
      label="UID"
      help-text="UID of type 00000000-0000-0000-0000-000000000000"
  />
  <AdminSelectorField
      @changeOption="(option: SelectorOption) => country = option"
      :is-required="true"
      :options="[{slug: 'test1', name: 'name1'}, {slug: 'test2', name: 'name2'}, {slug: 'test3', name: 'name3'}]"
      :has-search="true"
      label="Country"
  />
<!--  <div>market(Заполняется в зависимости от Страны; Фильтруется в зав от Страны; Селектор)</div>-->
  <AdminSelectorField
      @changeOption="(option: SelectorOption) => market = option"
      :is-required="true"
      :is-disabled="!country.slug.length"
      :options="[{slug: 'test1', name: 'name1'}, {slug: 'test2', name: 'name2'}, {slug: 'test3', name: 'name3'}]"
      :has-search="true"
      label="Market"
      help-text="Is unblocked after filling the country field"
  />
  <AdminSelectorField
      @changeOption="(option: SelectorOption) => sector = option"
      :is-required="true"
      :options="[{slug: 'test1', name: 'name1'}, {slug: 'test2', name: 'name2'}, {slug: 'test3', name: 'name3'}]"
      :has-search="true"
      label="Sector"
  />
<!--  <div>industry(Недоступен до выбора Сектора; Фильтруется в зав от Сектора; Селектор)</div>-->
  <AdminSelectorField
      @changeOption="(option: SelectorOption) => industry = option"
      :is-required="true"
      :is-disabled="!sector.slug.length"
      :options="[{slug: 'test1', name: 'name1'}, {slug: 'test2', name: 'name2'}, {slug: 'test3', name: 'name3'}]"
      :has-search="true"
      label="Industry"
  />
  <AdminImageField
      v-model="logo"
      label="Logo"
      help-text="Drag the photo into the input zone or click there to chose the photo"
  />

  <AdminTextField
      v-model="description"
      label="Description"
  />
  <AdminCheckBoxField
      v-model="isFund"
      label="Company is a fund"
  />
  <AdminCharField
      v-model="city"
      label="City"
  />
  <AdminCharField
      v-model="website"
      label="Website"
  />
  <AdminCharField
      v-model="founded"
      label="Founded"
      help-text="Year of company foundation"
  />

  <RoundedDarkBlueButton disabled>
    <span>Save</span>
  </RoundedDarkBlueButton>
</div>
</template>

<style scoped>

</style>