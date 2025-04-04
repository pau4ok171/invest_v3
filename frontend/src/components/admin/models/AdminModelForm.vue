<script lang="ts">
import { computed, defineComponent } from 'vue'
import axios from 'axios'
import type {
  AdminModelValue,
  IFetchedCountry,
  IFetchedIndustry,
  IFetchedMarket,
  IFetchedSector,
  IFormattedCountry,
  IFormattedDetailCompany,
  IFormattedIndustry,
  IFormattedMarket,
  IFormattedSector,
  IAdminField,
  IAdminModel,
  IAdminUnitedField,
  PreviousFormattedDetailCompany,
} from '@/types/admin.types'
import { useVuelidate } from '@vuelidate/core'
import getSlug from 'speakingurl'
import _ from 'lodash'
import {
  companyModel,
  defaultModelFieldData,
} from '@/components/admin/models/models'
import AdminField from '@/components/admin/models/fields/AdminField.vue'
import { useAdminStore } from '@/store/admin'
import {
  isAdminValidatorType,
  isBaseValidators,
  isKeyOfPreviousFormattedDetailCompany,
} from '@/types/admin.types'

export default defineComponent({
  name: 'AdminModelForm',
  components: {
    AdminField,
  },
  setup: () => {
    const store = useAdminStore()
    const v$ = useVuelidate({ $rewardEarly: true, $lazy: true })
    const watchCompanyFormData = computed(() => store.companyFormData)
    const watchEditModeActivated = computed(() => store.editModeActivated)

    return {
      v$,
      store,
      watchCompanyFormData,
      watchEditModeActivated,
    }
  },
  data() {
    return {
      sectors: [] as Array<IFormattedSector>,
      markets: [] as Array<IFormattedMarket>,
      industries: [] as Array<IFormattedIndustry>,
      countries: [] as Array<IFormattedCountry>,
    }
  },
  validations() {
    return {
      watchCompanyFormData: {
        ...Object.entries(this.model).reduce(
          (obj, [k, v]) => ({ [k]: v.validators, ...obj }),
          {}
        ),
      },
    }
  },
  async mounted() {
    if (!this.store.companyUID.length) {
      await this.store.activateEditMode()
      this.store.isNewModel = true
    } else {
      await this.store.deactivateEditMode()
      this.store.isNewModel = false
      await this.store.fetchCompany()
    }
    await this.fetchSelectorOptions()
  },
  async unmounted() {
    await this.store.deleteModelData()
  },
  computed: {
    model(): IAdminModel {
      const model = { ...companyModel }
      return Object.entries(model).reduce((acc, [key, fieldFromModel]) => {
        // Unite field with defaultField
        const field: IAdminUnitedField = Object.assign({
          ...defaultModelFieldData,
          ...fieldFromModel,
        })
        // MODEL VALUE
        field.modelValue = key
        // VALIDATORS
        if (isAdminValidatorType(field.validators)) {
          if (isBaseValidators(field.validators)) {
            field.isRequired = Object.hasOwn(field.validators, 'required')
          } else {
            field.isRequired = Object.hasOwn(field.validators.slug, 'required')
          }
        }
        // OPTIONS
        if (field.options && typeof field.options === 'string') {
          field.options = (this as any)[field.options]
        }
        return { ...acc, [key]: field }
      }, {})
    },
    filteredMarkets() {
      return [...this.markets].filter(
        (m: IFormattedMarket) =>
          m.key === this.store.companyFormData.country.key
      )
    },
    filteredIndustries() {
      return [...this.industries].filter(
        (i: IFormattedIndustry) =>
          i.key === this.store.companyFormData.sector.key
      )
    },
  },
  methods: {
    getModelValue(m: IAdminField) {
      return this.store.companyFormData[
        m.modelValue as keyof IFormattedDetailCompany
      ]
    },
    updateModel(field: IAdminField, value: AdminModelValue) {
      const key = field.modelValue
      let companyFormData = { ...this.store.companyFormData }

      companyFormData = { ...companyFormData, [key]: value }

      // DEPENDING FIELDS
      if (key === 'ticker' && typeof value === 'string')
        companyFormData['slug'] = getSlug(_.kebabCase(value))
      if (key === 'country')
        companyFormData['market'] = { name: '', slug: '', key: 0 }
      if (key === 'sector')
        companyFormData['industry'] = { name: '', slug: '', key: 0 }
      // END DEPENDING FIELDS
      this.store.companyFormData = companyFormData
    },
    async fetchSelectorOptions() {
      const selectorOptions = await axios
        .get('api/v1/admin/selector_options/')
        .then((r) => r.data)
        .catch((e) => console.log(e))
      this.countries = selectorOptions['countries'].map(
        (c: IFetchedCountry): IFormattedCountry => ({
          name: c.name,
          slug: c.name_iso,
          key: c.id,
          flagURL: c.flag_url,
          currency: c.currency,
        })
      )
      this.markets = selectorOptions['markets'].map(
        (m: IFetchedMarket): IFormattedMarket => ({
          name: m.title,
          slug: m.slug,
          key: m.country,
        })
      )
      this.sectors = selectorOptions['sectors'].map(
        (s: IFetchedSector): IFormattedSector => ({
          name: s.title,
          slug: s.slug,
          key: s.id,
        })
      )
      this.industries = selectorOptions['industries'].map(
        (i: IFetchedIndustry): IFormattedIndustry => ({
          name: i.title,
          slug: i.slug,
          key: i.sector,
        })
      )
    },
    async proceedModelSaving() {
      const isFormCorrect = await this.v$.$validate()
      if (!isFormCorrect) return

      await this.store.saveModelForm()
    },
    resetField(key: '__all__' | string) {
      this.store.resetField(key)

      if (key === '__all__') {
        this.v$.watchCompanyFormData.$reset()
      } else if (key === 'country') {
        this.v$.watchCompanyFormData[key].$reset()
        this.v$.watchCompanyFormData['market'].$reset()
      } else if (key === 'sector') {
        this.v$.watchCompanyFormData[key].$reset()
        this.v$.watchCompanyFormData['industry'].$reset()
      } else {
        this.v$.watchCompanyFormData[key].$reset()
      }
    },
  },
  watch: {
    watchCompanyFormData: {
      handler(companyFormData: IFormattedDetailCompany) {
        // Check if values in CompanyFormData was modified
        if (this.store.editModeActivated) {
          const previousCompanyFormData: PreviousFormattedDetailCompany = {
            ...this.store.previousCompanyFormData,
          }

          Object.entries(companyFormData).forEach(([k, v]) => {
            if (
              isKeyOfPreviousFormattedDetailCompany(previousCompanyFormData, k)
            ) {
              const value = previousCompanyFormData[k].value
              if (typeof value == 'object' && 'slug' in value) {
                previousCompanyFormData[k].wasModified = value.slug !== v.slug
                return
              }
              previousCompanyFormData[k].wasModified = value !== v
            }
          })
        }
      },
      deep: true,
    },
    watchEditModeActivated(val) {
      // If editMode was activated
      if (val === true) {
        this.v$.$commit()
      }
    },
  },
})
</script>

<template>
  <div class="admin-model__admin-model-form">
    <div class="admin-model-form__reset-button-wrapper">
      <v-btn
        icon="$iReset"
        color="info"
        rounded="lg"
        density="comfortable"
        v-show="store.getModelWasModified"
        @click="store.resetField('__all__')"
        v-tippy="{ content: 'Click to reset all changes' }"
      />
    </div>

    <AdminField
      v-for="m in model"
      :key="m.modelValue"
      :field="m.field"
      :model-value="getModelValue(m)"
      @update:model-value="(value: any) => updateModel(m, value)"
      @resetField="resetField(m.modelValue)"
      @touch="v$.watchCompanyFormData[m.modelValue].$touch"
      @commitValidator="v$.watchCompanyFormData[m.modelValue].$commit"
      :is-required="m.isRequired"
      :is-disabled="
        typeof m.isDisabled == 'string'
          ? !store[m.isDisabled as keyof typeof store]
          : m.isDisabled
      "
      :label="m.label"
      :help-text="m.helpText"
      :options="m.options"
      :has-search="m.hasSearch"
      :errors="v$.watchCompanyFormData[m.modelValue].$errors"
      :is-dirty="v$.watchCompanyFormData[m.modelValue].$dirty"
      :was-modified="
        m.wasModifiedIsNeeded
          ? store.previousCompanyFormData[m.modelValue].wasModified
          : false
      "
    />

    <v-btn
      text="save"
      color="info"
      rounded="lg"
      block
      :loading="store.modelIsSaving"
      :disabled="v$.$invalid || !store.getModelWasModified"
      @click="proceedModelSaving"
    />
  </div>
</template>

<style scoped lang="scss">
.admin-model__admin-model-form {
  position: relative;
  background-color: #1b222d;
  border-radius: 8px;
  padding: 24px 32px;
}
.admin-model-form__reset-button-wrapper {
  position: absolute;
  top: 24px;
  right: 32px;
}
</style>
