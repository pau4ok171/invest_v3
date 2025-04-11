<script setup lang="ts">
// Components
import AdminModelFields from '@/components/admin/models/AdminModelFields.vue'

// Composables
import { useAdminModelStore } from '@/store/admin/admin'

// Utilities
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { helpers, numeric, required, url } from '@vuelidate/validators'
import {
  isImageValidator,
  isYearValidator,
  maxVolumeValidator,
} from '@/components/admin/models/validators'

// Types
import type {
  BaseField,
  EnrichedFormField,
  FormField,
} from '@/components/admin/models/types'
import type {
  IFetchedCountry,
  IFetchedIndustry,
  IFetchedMarket,
  IFetchedSector,
  IFormattedCountry,
  IFormattedIndustry,
  IFormattedMarket,
  IFormattedSector,
} from '@/types/admin.types'

const store = useAdminModelStore()

const sectors = ref<IFormattedSector[]>([])
const markets = ref<IFormattedMarket[]>([])
const industries = ref<IFormattedIndustry[]>([])
const countries = ref<IFormattedCountry[]>([])
const filteredMarkets = computed<IFormattedMarket[]>(() =>
  markets.value.filter((m) => m.parentKey === store.formState.country.key)
)
const filteredIndustries = computed<IFormattedIndustry[]>(() =>
  industries.value.filter((m) => m.parentKey === store.formState.sector.key)
)

const defaultField: BaseField = {
  key: 'isVisible',
  type: 'text',
  label: '',
  helpText: '',
  hasReset: true,
  validators: {},
}

const companyFields = computed<FormField[]>(
  () =>
    [
      {
        key: 'isVisible',
        type: 'checkbox',
        label: 'Company is publicly visible',
      },
      {
        key: 'ticker',
        type: 'text',
        label: 'Ticker',
        validators: { required },
      },
      {
        key: 'slug',
        type: 'text',
        label: 'Slug',
        hasReset: false,
        validators: { required },
      },
      {
        key: 'uid',
        type: 'text',
        label: 'UID',
        helpText: 'UID of type 00000000-0000-0000-0000-000000000000',
        validators: { required },
      },
      {
        key: 'companyName',
        type: 'text',
        label: 'Company Name',
        validators: { required },
      },
      {
        key: 'shortCompanyName',
        type: 'text',
        label: 'Short Company Name',
      },
      {
        key: 'shortCompanyNameGenitive',
        type: 'text',
        label: 'Short Company Name Genitive',
      },
      {
        key: 'description',
        type: 'textarea',
        label: 'Description',
      },
      {
        key: 'shortDescription',
        type: 'textarea',
        label: 'Short Description',
      },
      {
        key: 'country',
        type: 'selector',
        label: 'Country',
        items: countries.value,
        validators: {
          required: helpers.withMessage(
            'Country is required',
            (value: { slug: string }) => !!value.slug.length
          ),
        },
      },
      {
        key: 'market',
        type: 'selector',
        label: 'Market',
        helpText: 'Is unblocked after filling the country field',
        items: filteredMarkets.value,
        validators: {
          required: helpers.withMessage(
            'Market is required',
            (value: { slug: string }) => !!value.slug.length
          ),
        },
      },
      {
        key: 'sector',
        type: 'selector',
        label: 'Sector',
        items: sectors.value,
        validators: {
          required: helpers.withMessage(
            'Sector is required',
            (value: { slug: string }) => !!value.slug.length
          ),
        },
      },
      {
        key: 'industry',
        type: 'selector',
        label: 'Industry',
        helpText: 'Is unblocked after filling the sector field',
        items: filteredIndustries.value,
        validators: {
          required: helpers.withMessage(
            'Industry is required',
            (value: { slug: string }) => !!value.slug.length
          ),
        },
      },
      {
        key: 'logo',
        type: 'image',
        label: 'Logo',
        validators: {
          isImageValidator: helpers.withMessage(
            'Field must be an image',
            isImageValidator
          ),
          maxVolumeValidator: helpers.withMessage(
            'Field must be 100Kb max',
            maxVolumeValidator
          ),
        },
      },
      {
        key: 'isFund',
        type: 'checkbox',
        label: 'Company is a fund',
      },
      { key: 'city', type: 'text', label: 'City' },
      { key: 'website', type: 'text', label: 'Website', validators: { url } },
      {
        key: 'founded',
        type: 'text',
        label: 'Founded',
        helpText: 'Year of company foundation',
        validators: {
          numeric,
          isYearValidator: helpers.withMessage(
            `Field must be an year between 1000 and ${new Date().getFullYear()}`,
            isYearValidator
          ),
        },
      },
    ] as FormField[]
)

const items = computed<EnrichedFormField[]>(() => {
  return companyFields.value.map(
    (item) =>
      ({
        ...defaultField,
        ...item,
      }) as EnrichedFormField
  )
})

async function fetchSelectors() {
  try {
    const response = await axios.get('api/v1/admin/selector_options/')

    const selectors = response.data

    countries.value = selectors['countries'].map(
      (c: IFetchedCountry): IFormattedCountry => ({
        name: c.name,
        slug: c.name_iso,
        key: c.id,
        flagURL: c.flag_url,
        currency: c.currency,
      })
    )
    markets.value = selectors['markets'].map(
      (m: IFetchedMarket): IFormattedMarket => ({
        name: m.title,
        slug: m.slug,
        parentKey: m.country,
      })
    )
    sectors.value = selectors['sectors'].map(
      (s: IFetchedSector): IFormattedSector => ({
        name: s.title,
        slug: s.slug,
        key: s.id,
      })
    )
    industries.value = selectors['industries'].map(
      (i: IFetchedIndustry): IFormattedIndustry => ({
        name: i.title,
        slug: i.slug,
        parentKey: i.sector,
      })
    )
  } catch (e) {
    console.log(e)
  }
}

onMounted(() => {
  const init = async () => {
    await fetchSelectors()
  }

  init()
})
</script>

<template>
  <v-card>
    <v-card-item style="width: 50%">
      <v-form>
        <admin-model-fields :items />
      </v-form>
    </v-card-item>
  </v-card>
</template>
