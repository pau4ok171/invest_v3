<script lang="ts">
import {defineComponent} from 'vue'
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
import AdminField from "@/components/admin/models/fields/AdminField.vue";

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
    AdminField,
    AtomSpinner,
    RoundedDarkBlueButton,
    ResetIcon,
  },
  setup: () => ({ v$: useVuelidate({ $rewardEarly: true, $lazy: true })}),
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
  
  <AdminField
    v-for="m in model"
    :key="m.modelValue"
    :field="m.field"
    :model-value="companyFormData[m.modelValue]"
    @update:model-value="(value: any) => updateModel(m.modelValue, value)"
    @resetField="resetField(m.modelValue)"
    @touch="v$.companyFormData[m.modelValue].$touch"
    @commitValidator="v$.companyFormData[m.modelValue].$commit"
    :is-required="m.isRequired"
    :is-disabled="m.isDisabled"
    :label="m.label"
    :help-text="m.helpText"
    :options="m.options"
    :has-search="m.hasSearch"
    :errors="v$.companyFormData[m.modelValue].$errors"
    :was-modified="m.wasModifiedIsNeeded?previousCompanyFormData[m.modelValue].wasModified:false"
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