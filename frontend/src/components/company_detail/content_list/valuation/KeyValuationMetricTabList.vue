<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref, watch } from 'vue'

// Types
import type { PropType } from 'vue'
import type { FairValueTab } from '@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue'

const props = defineProps({
  tabs: {
    type: Object as PropType<FairValueTab[]>,
    required: true,
  },
  selected: {
    type: Object as PropType<FairValueTab>,
    required: true,
  },
})

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const emit = defineEmits()

const modelValue = ref(0)
const { t } = useI18n()
const metric = computed(() => {
  const ticker = company.value.ticker || 'Company'
  return props.selected
    ? t(
        `companyDetail.valuation.keyValuationMetric.${props.selected.id}Metric`,
        { ticker }
      )
    : ''
})

watch(modelValue, (value) => {
  emit('update:selected', props.tabs[value])
})
</script>

<template>
  <div>
    <v-btn-toggle
      class="mb-4"
      v-model="modelValue"
      variant="outlined"
      density="comfortable"
      mandatory
      selected-class="text-info"
    >
      <v-btn
        v-for="tab in tabs"
        :key="`key-valuation-tab-${tab.id}`"
        :text="tab.name"
      />
    </v-btn-toggle>

    <v-banner bg-color="surface-bright" rounded border="0">
      <template #prepend>
        <v-icon icon="$iSolidStar" color="info" size="24" />
      </template>

      <v-banner-text>
        <span class="text-info mr-1"
          >{{
            t('companyDetail.valuation.keyValuationMetric.keyMetric')
          }}:</span
        >
        <span>{{ metric }}</span>
      </v-banner-text>
    </v-banner>
  </div>
</template>
