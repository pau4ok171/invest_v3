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
import {useVuelidate} from "@vuelidate/core";
import getSlug from "speakingurl";
import _ from "lodash";
import {companyModel, defaultModelFieldData} from "@/components/admin/models/models";
import {AtomSpinner} from "epic-spinners";

const getModel = () => {
  const model: any = {...companyModel}
  Object.keys(model).forEach((k) => {
    model[k] = Object.assign({...defaultModelFieldData}, model[k])
    model[k].modelValue = k
    if (Object.hasOwn(model[k].validators, 'slug')) {
      model[k].isRequired = Object.hasOwn(model[k].validators.slug, 'required')
    } else {
      model[k].isRequired = Object.hasOwn(model[k].validators, 'required')
    }
  })
  return model
}

export default defineComponent({
  name: "AdminModelForm",
  components: {
    AtomSpinner,
    RoundedDarkBlueButton,
    ResetIcon,
    AdminImageField,
    AdminSelectorField,
    AdminCheckBoxField,
    AdminTextField,
    AdminCharField
  },
  setup: () => ({ v$: useVuelidate({ $autoDirty: true, $rewardEarly: true })}),
  data() {
    return {
      sectors: [] as Array<FormattedSector>,
      markets: [] as Array<FormattedMarket>,
      industries: [] as Array<FormattedIndustry>,
      countries: [] as Array<FormattedCountry>,
    }
  },
  validations () {
    return {
      companyFormData: {
        ...Object.entries(getModel()).reduce((obj, [k, v]: [string, any]) => ({[k]: v.validators, ...obj}), {})
      },
    }
  },
  async mounted() {
    if (!this.companyUID.length) {
      await this.activateEditMode()
      this.setIsNewModel(true)
      } else {
      await this.deactivateEditMode()
      this.setIsNewModel(false)
      await this.fetchCompanyByUID(this.companyUID)
    }
    await this.fetchSelectorOptions()
  },
  async unmounted() {
    await this.deleteModelData()
  },
  computed: {
    ...mapState({
      companyFormData: (state: any) => state.adminModule.companyFormData,
      modelIsSaving: (state: any) => state.adminModule.modelIsSaving,
      isNewModel: (state: any) => state.adminModule.isNewModel,
    }),
    ...mapGetters({
      companyUID: 'adminModule/getCompanyUID',
      editModeActivated: 'adminModule/getEditModeActivated',
      modelWasModified: 'adminModule/getModelWasModified',
      previousCompanyFormData: 'adminModule/getPreviousCompanyFormData',
    }),
    model() {
      const model = getModel()
      Object.entries(model).forEach(([k, v]: [k: string, v: any]) => {
        if (v.options) {
          model[k].options = (this as any)[v.options]
        }
        if(typeof v.isDisabled === "string") {
            model[k].isDisabled = v.isDisabled.startsWith('!') ? !(this as any)[v.isDisabled.slice(1)] : (this as any)[v.isDisabled]
        } else {
          model[k].isDisabled = v.isDisabled
        }
      })
      return model
    },
    filteredMarkets() {
      return [...this.markets].filter((m: FormattedMarket) => m.key === this.companyFormData.country.key)
    },
    filteredIndustries() {
      return [...this.industries].filter((i: FormattedIndustry) => i.key === this.companyFormData.sector.key)
    },
  },
  methods: {
    ...mapMutations({
      setCompanyFormData: 'adminModule/setCompanyFormData',
      setEditModeActivated: 'adminModule/setEditModeActivated',
      setIsNewModel: 'adminModule/setIsNewModel',
    }),
    ...mapActions({
      fetchCompanyByUID: 'adminModule/fetchCompany',
      saveModelForm: 'adminModule/saveModelForm',
      deleteModelData: 'adminModule/deleteModelData',
      activateEditMode: 'adminModule/activateEditMode',
      deactivateEditMode: 'adminModule/deactivateEditMode',
      resetField: 'adminModule/resetField',
    }),
    updateModel(key: string, value: any) {
      const companyFormData = {...this.companyFormData}
      companyFormData[key] = value
      // DEPENDING FIELDS
      if (key === 'ticker') companyFormData['slug'] = getSlug(_.kebabCase(value))
      if (key === 'country') companyFormData['market'] = {name: '', slug: '', key: ''}
      if (key === 'sector') companyFormData['industry'] = {name: '', slug: '', key: ''}
      // END DEPENDING FIELDS
      this.setCompanyFormData(companyFormData)
    },
    async fetchSelectorOptions() {
      const selectorOptions = await axios.get('api/v1/admin/selector_options/').then(r => r.data).catch(e => console.log(e))
      this.countries = selectorOptions['countries'].map((c: FetchedCountry): FormattedCountry => ({name: c.name, slug: c.name_iso, key: c.id, flagURL: c.flag_url, currency: c.currency}))
      this.markets = selectorOptions['markets'].map((m: FetchedMarket): FormattedMarket => ({name: m.title, slug: m.slug, key: m.country}))
      this.sectors = selectorOptions['sectors'].map((s: FetchedSector): FormattedSector => ({name: s.title, slug: s.slug, key: s.id}))
      this.industries = selectorOptions['industries'].map((i: FetchedIndustry): FormattedIndustry => ({name: i.title, slug: i.slug, key: i.sector}))
    },
    async proceedModelSaving() {
      const isFormCorrect = await this.v$.$validate()
      if (!isFormCorrect) return

      await this.saveModelForm()
    },
  },
  watch: {
    companyFormData: {
      handler(companyFormData) {
        // Check if values in CompanyFormData was modified
        if (this.editModeActivated) {
          const previousCompanyFormData = {...this.previousCompanyFormData}

          Object.entries(companyFormData).forEach(([k, v]: [k: string, v: any]) => {
            if (Object.hasOwn(previousCompanyFormData[k].value, 'slug')) {
              previousCompanyFormData[k].wasModified = previousCompanyFormData[k].value.slug !== v.slug
              return
            }
            previousCompanyFormData[k].wasModified = previousCompanyFormData[k].value !== v
          })
        }
        console.log(this.v$)
        console.log(this.v$.companyFormData.$errors)
      },
      deep: true
    },
    editModeActivated(val) {
      // If editMode was activated
      if (val === true) {
        this.v$.$commit()
      }
    }
  },
})

const isImageValidator = (file: File) => {
  if (!file?.size) return true
  return file.type.startsWith('image')
}
const maxVolumeValidator = (file: File|Object) => {
  if (file instanceof File && file.type.startsWith('image')) {
    return file.size < 100 * 1024
  }
  return true
}
const isYearValidator = (val: any) => {
  return val.length === 4 || val.length === 0
}
</script>

<template>
<div class="admin-model__admin-model-form">
  <button
      class="admin-model-form__reset-button"
      v-show="modelWasModified"
      @click="resetField('__all__')"
      v-tippy="{content: 'Click to reset all changes'}"
  >
    <ResetIcon/>
  </button>
  <AdminCheckBoxField
      :model-value="companyFormData.isVisible"
      @update:model-value="setIsVisible"
      @resetField="resetField('isVisible')"
      @commitValidator="v$.companyFormData.isVisible.$commit()"
      :wasModified="previousCompanyFormData.isVisible.wasModified"
      :is-disabled="!editModeActivated"
      label="Company is publicly visible"
  />
  <AdminCharField
      :model-value="companyFormData.ticker"
      @update:model-value="setTicker"
      @resetField="resetField('ticker')"
      :wasModified="previousCompanyFormData.ticker.wasModified"
      @commitValidator="v$.companyFormData.ticker.$commit()"
      :is-required="true"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.ticker.$errors"
      label="Ticker"
  />
  <AdminCharField
      :model-value="companyFormData.slug"
      @update:model-value="setSlug"
      @commitValidator="v$.companyFormData.slug.$commit()"
      :is-disabled="true"
      label="Slug"
  />
  <AdminCharField
      :model-value="companyFormData.uid"
      @update:model-value="setUID"
      @resetField="resetField('uid')"
      :wasModified="previousCompanyFormData.uid.wasModified"
      @commitValidator="v$.companyFormData.uid.$commit()"
      :is-required="true"
      :errors="v$.companyFormData.uid.$errors"
      :is-disabled="!editModeActivated"
      label="UID"
      help-text="UID of type 00000000-0000-0000-0000-000000000000"
  />
  <AdminCharField
      :model-value="companyFormData.companyName"
      @update:model-value="setCompanyName"
      @resetField="resetField('companyName')"
      :wasModified="previousCompanyFormData.companyName.wasModified"
      @commitValidator="v$.companyFormData.companyName.$commit()"
      :is-required="true"
      :errors="v$.companyFormData.companyName.$errors"
      :is-disabled="!editModeActivated"
      label="Company Name"
  />
  <AdminCharField
      :model-value="companyFormData.shortCompanyName"
      @update:model-value="setShortCompanyName"
      @resetField="resetField('shortCompanyName')"
      @commitValidator="v$.companyFormData.shortCompanyName.$commit()"
      :wasModified="previousCompanyFormData.shortCompanyName.wasModified"
      :is-disabled="!editModeActivated"
      label="Short Company Name"
  />
  <AdminCharField
      :model-value="companyFormData.shortCompanyNameGenitive"
      @update:model-value="setShortCompanyNameGenitive"
      @resetField="resetField('shortCompanyNameGenitive')"
      @commitValidator="v$.companyFormData.shortCompanyNameGenitive.$commit()"
      :wasModified="previousCompanyFormData.shortCompanyNameGenitive.wasModified"
      :is-disabled="!editModeActivated"
      label="Short Company Name Genitive"
  />
  <AdminTextField
      :model-value="companyFormData.description"
      @update:model-value="setDescription"
      @resetField="resetField('description')"
      @commitValidator="v$.companyFormData.description.$commit()"
      :wasModified="previousCompanyFormData.description.wasModified"
      :is-disabled="!editModeActivated"
      label="Description"
  />
  <AdminTextField
      :model-value="companyFormData.shortDescription"
      @update:model-value="setShortDescription"
      @resetField="resetField('shortDescription')"
      @commitValidator="v$.companyFormData.shortDescription.$commit()"
      :wasModified="previousCompanyFormData.shortDescription.wasModified"
      :is-disabled="!editModeActivated"
      label="Short Description"
  />
  <AdminSelectorField
      :model-value="companyFormData.country"
      @update:model-value="setCountry"
      @resetField="resetField('country')"
      @commitValidator="v$.companyFormData.country.$commit()"
      :wasModified="previousCompanyFormData.country.wasModified"
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
      @resetField="resetField('market')"
      @commitValidator="v$.companyFormData.market.$commit()"
      :wasModified="previousCompanyFormData.market.wasModified"
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
      @resetField="resetField('sector')"
      @commitValidator="v$.companyFormData.sector.$commit()"
      :wasModified="previousCompanyFormData.sector.wasModified"
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
      @resetField="resetField('industry')"
      @commitValidator="v$.companyFormData.industry.$commit()"
      :wasModified="previousCompanyFormData.industry.wasModified"
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
      @resetField="resetField('logo')"
      @commitValidator="v$.companyFormData.logo.$commit()"
      :wasModified="previousCompanyFormData.logo.wasModified"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.logo.$errors"
      help-text="Drag the photo into the input zone or click there to chose the photo"
      label="Logo"
  />
  <AdminCheckBoxField
      :model-value="companyFormData.isFund"
      @update:model-value="setIsFund"
      @resetField="resetField('isFund')"
      @commitValidator="v$.companyFormData.isFund.$commit()"
      :wasModified="previousCompanyFormData.isFund.wasModified"
      :is-disabled="!editModeActivated"
      label="Company is a fund"
  />
  <AdminCharField
      :model-value="companyFormData.city"
      @update:model-value="setCity"
      @resetField="resetField('city')"
      @commitValidator="v$.companyFormData.city.$commit()"
      :wasModified="previousCompanyFormData.city.wasModified"
      :is-disabled="!editModeActivated"
      label="City"
  />
  <AdminCharField
      :model-value="companyFormData.website"
      @update:model-value="setWebsite"
      @resetField="resetField('website')"
      @commitValidator="v$.companyFormData.website.$commit()"
      :wasModified="previousCompanyFormData.website.wasModified"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.website.$errors"
      label="Website"
  />
  <AdminCharField
      :model-value="companyFormData.founded"
      @update:model-value="setFounded"
      @resetField="resetField('founded')"
      @commitValidator="v$.companyFormData.founded.$commit()"
      :wasModified="previousCompanyFormData.founded.wasModified"
      :is-disabled="!editModeActivated"
      :errors="v$.companyFormData.founded.$errors"
      label="Founded"
      help-text="Year of company foundation"
  />

  <RoundedDarkBlueButton :is-full-width="true" :disabled="v$.$invalid || modelIsSaving || !modelWasModified" @click="proceedModelSaving()">
    <atom-spinner
      v-show="modelIsSaving"
      :animation-duration="1250"
      :size="30"
      color="#ff1d5e"
    />
    <span v-if="!modelIsSaving">Save</span>
    <span v-else>Saving...</span>
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