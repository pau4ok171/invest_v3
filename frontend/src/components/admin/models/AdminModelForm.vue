<script lang="ts">
import {defineComponent} from 'vue'
import AdminCharField from "@/components/admin/models/fields/AdminCharField.vue";
import AdminTextField from "@/components/admin/models/fields/AdminTextField.vue";
import AdminCheckBoxField from "@/components/admin/models/fields/AdminCheckBoxField.vue";
import AdminSelectorField from "@/components/admin/models/fields/AdminSelectorField.vue";
import AdminImageField from "@/components/admin/models/fields/AdminImageField.vue";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import type {
  FetchedCountry,
  FetchedIndustry,
  FetchedMarket,
  FetchedSector,
  FormattedCountry,
  FormattedIndustry,
  FormattedMarket,
  FormattedSector,
} from "@/types/admin";
import ResetIcon from "@/components/icons/ResetIcon.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import { useVuelidate } from '@vuelidate/core'
import {required, url, numeric, helpers} from "@vuelidate/validators";

export default defineComponent({
  name: "AdminModelForm",
  components: {
    RoundedDarkBlueButton,
    ResetIcon,
    AdminImageField,
    AdminSelectorField,
    AdminCheckBoxField,
    AdminTextField,
    AdminCharField
  },
  setup() {
    return {
      v$: useVuelidate({ $lazy: true, $autoDirty: true })
    }
  },
  data() {
    return {
      sectors: [] as Array<FormattedSector>,
      markets: [] as Array<FormattedMarket>,
      industries: [] as Array<FormattedIndustry>,
      countries: [] as Array<FormattedCountry>,
      formModified: false,
      isNewRecord: false,
    }
  },
  validations () {
    return {
      companyFormData: {
        ticker: { required },
        uid: { required },
        companyName: { required },
        country: { slug: { required } },
        market: { slug: { required } },
        sector: { slug: { required } },
        industry: { slug: { required } },
        logo: { isImageValidator: helpers.withMessage('Logo must be an image', isImageValidator) },
        website: { url },
        founded: { numeric },
      }
    }
  },
  props: {
    editModeActivated: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    ...mapState({
      companyFormData: state => state.adminModule.companyFormData,
    }),
    ...mapGetters({
      companyUID: 'adminModule/getCompanyUID',
    }),
    filteredMarkets() {
      return [...this.markets].filter((m: FormattedMarket) => m.key === this.companyFormData.country.key)
    },
    filteredIndustries() {
      return [...this.industries].filter((i: FormattedIndustry) => i.key === this.companyFormData.sector.key)
    },
  },
  async mounted() {
    if (!this.companyUID.length) {
      this.isNewRecord = true
      this.$emit('update:editModeActivated', true)
    } else {
      this.isNewRecord = false
      this.$emit('update:editModeActivated', false)
      await this.fetchCompanyByUID(this.companyUID)
    }
    await this.fetchSelectorOptions()
  },
  methods: {
    ...mapMutations({
      setIsVisible: 'adminModule/setCompanyModelIsVisible',
      setCompanyName: 'adminModule/setCompanyModelCompanyName',
      setShortCompanyName: 'adminModule/setCompanyModelShortCompanyName',
      setShortCompanyNameGenitive: 'adminModule/setCompanyModelShortCompanyNameGenitive',
      setTicker: 'adminModule/setCompanyModelTicker',
      setSlug: 'adminModule/setCompanyModelSlug',
      setUID: 'adminModule/setCompanyModelUID',
      setCountry: 'adminModule/setCompanyModelCountry',
      setMarket: 'adminModule/setCompanyModelMarket',
      setSector: 'adminModule/setCompanyModelSector',
      setIndustry: 'adminModule/setCompanyModelIndustry',
      setLogo: 'adminModule/setCompanyModelLogo',
      setDescription: 'adminModule/setCompanyModelDescription',
      setShortDescription: 'adminModule/setCompanyModelShortDescription',
      setIsFund: 'adminModule/setCompanyModelIsFund',
      setCity: 'adminModule/setCompanyModelCity',
      setWebsite: 'adminModule/setCompanyModelWebsite',
      setFounded: 'adminModule/setCompanyModelFounded',
    }),
    ...mapActions({
      fetchCompanyByUID: 'adminModule/fetchCompany',
    }),
    async fetchSelectorOptions() {
      const selectorOptions = await axios.get('api/v1/admin/selector_options/').then(r => r.data).catch(e => console.log(e))
      this.countries = selectorOptions['countries'].map((c: FetchedCountry): FormattedCountry => ({name: c.name, slug: c.name_iso, key: c.id, flagURL: c.flag_url, currency: c.currency}))
      this.markets = selectorOptions['markets'].map((m: FetchedMarket): FormattedMarket => ({name: m.title, slug: m.slug, key: m.country}))
      this.sectors = selectorOptions['sectors'].map((s: FetchedSector): FormattedSector => ({name: s.title, slug: s.slug, key: s.id}))
      this.industries = selectorOptions['industries'].map((i: FetchedIndustry): FormattedIndustry => ({name: i.title, slug: i.slug, key: i.sector}))
    },
  },
})

const isImageValidator = (file: File) => {
  if (!file?.size) return true
  return file.type.startsWith('image')
}
</script>

<template>
<div class="admin-model__admin-model-form">
  <button
      class="admin-model-form__reset-button"
      v-tippy="{content: 'Click to reset all changes'}"
  >
    <ResetIcon/>
  </button>

  <AdminCheckBoxField
      :model-value="companyFormData.isVisible"
      @update:model-value="setIsVisible"
      :is-disabled="!editModeActivated"
      label="Company is publicly visible"
  />
  <AdminCharField
      :model-value="companyFormData.ticker"
      @update:model-value="setTicker"
      :is-required="true"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.ticker.$errors"
      label="Ticker"
  />
  <AdminCharField
      :model-value="companyFormData.slug"
      @update:model-value="setSlug"
      :is-disabled="true"
      label="Slug"
  />
  <AdminCharField
      :model-value="companyFormData.uid"
      @update:model-value="setUID"
      :is-required="true"
      :errors="v$.companyFormData.uid.$errors"
      :is-disabled="!editModeActivated"
      label="UID"
      help-text="UID of type 00000000-0000-0000-0000-000000000000"
  />
  <AdminCharField
      :model-value="companyFormData.companyName"
      @update:model-value="setCompanyName"
      :is-required="true"
      :errors="v$.companyFormData.companyName.$errors"
      :is-disabled="!editModeActivated"
      label="Company Name"
  />
  <AdminCharField
      :model-value="companyFormData.shortCompanyName"
      @update:model-value="setShortCompanyName"
      :is-disabled="!editModeActivated"
      label="Short Company Name"
  />
  <AdminCharField
      :model-value="companyFormData.shortCompanyNameGenitive"
      @update:model-value="setShortCompanyNameGenitive"
      :is-disabled="!editModeActivated"
      label="Short Company Name Genitive"
  />
  <AdminTextField
      :model-value="companyFormData.description"
      @update:model-value="setDescription"
      :is-disabled="!editModeActivated"
      label="Description"
  />
  <AdminTextField
      :model-value="companyFormData.shortDescription"
      @update:model-value="setShortDescription"
      :is-disabled="!editModeActivated"
      label="Short Description"
  />
  <AdminSelectorField
      :model-value="companyFormData.country"
      @update:model-value="setCountry"
      :is-required="true"
      :errors="v$.companyFormData.country.$errors"
      :is-disabled="!editModeActivated"
      :options="countries"
      :has-search="true"
      label="Country"
  />
  <AdminSelectorField
      :model-value="companyFormData.market"
      @update:model-value="setMarket"
      :is-required="true"
      :is-disabled="!companyFormData.country?.slug.length || !editModeActivated"
      :errors="v$.companyFormData.market.$errors"
      :options="filteredMarkets"
      :has-search="true"
      label="Market"
      help-text="Is unblocked after filling the country field"
  />
  <AdminSelectorField
      :model-value="companyFormData.sector"
      @update:model-value="setSector"
      :is-required="true"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.sector.$errors"
      :options="sectors"
      :has-search="true"
      label="Sector"
  />
  <AdminSelectorField
      :model-value="companyFormData.industry"
      @update:model-value="setIndustry"
      :is-required="true"
      :is-disabled="!companyFormData.sector?.slug.length || !editModeActivated"
      :errors="v$.companyFormData.industry.$errors"
      :options="filteredIndustries"
      :has-search="true"
      label="Industry"
      help-text="Is unblocked after filling the sector field"
  />
  <AdminImageField
      :model-value="companyFormData.logo"
      @update:model-value="setLogo"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.logo.$errors"
      help-text="Drag the photo into the input zone or click there to chose the photo"
      label="Logo"
  />
  <AdminCheckBoxField
      :model-value="companyFormData.isFund"
      @update:model-value="setIsFund"
      :is-disabled="!editModeActivated"
      label="Company is a fund"
  />
  <AdminCharField
      :model-value="companyFormData.city"
      @update:model-value="setCity"
      :is-disabled="!editModeActivated"
      label="City"
  />
  <AdminCharField
      :model-value="companyFormData.website"
      @update:model-value="setWebsite"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.website.$errors"
      label="Website"
  />
  <AdminCharField
      :model-value="companyFormData.founded"
      @update:model-value="setFounded"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.founded.$errors"
      label="Founded"
      help-text="Year of company foundation"
  />

  <RoundedDarkBlueButton :is-full-width="true" :disabled="v$.$invalid">
    <span>Save</span>
  </RoundedDarkBlueButton>
</div>
</template>

<style scoped lang="scss">
.admin-model__admin-model-form {
  position: relative;
  background-color: #1b222d;
  border-radius: 8px;
  padding: 24px 32px;
}
.admin-model-form__reset-button {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 24px;
  right: 32px;
  padding: 5px;
  border: 1px solid transparent;
  border-radius: 16px;
  background-color: rgba(53, 110, 233, .1);
  transition: background-color .4s;
  cursor: pointer;

  &:hover {
    background-color: rgba(53, 110, 233, .2);
  }

  & svg {
    fill: var(--blue);
    width: 32px;
    height: 32px;
    user-select: none;
  }
}
</style>