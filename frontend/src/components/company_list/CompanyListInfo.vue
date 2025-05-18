<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

// Types
import type { CountryState } from '@/store/companyList/types'

const store = useCompanyListStore()
const countryState = computed<CountryState>(() => store.countryState)
const { t } = useI18n()
</script>

<template>
  <div class="mt-4">
    <div class="text-h5 mb-2">
      Largest {{ store.countryState.title }} Stocks
    </div>

    <div class="text-caption mb-2">
      <span class="text-medium-emphasis text-uppercase mr-1">
        {{ t('common.updated') }}
      </span>
      <v-skeleton-loader
        class="d-inline-block mt-n3"
        v-if="store.fetching"
        width="120"
        type="text"
      />
      <template v-else>
        {{
          store.lastUpdate
            ? new Date(store.lastUpdate).toLocaleDateString('ru-RU')
            : 'n/a'
        }}
      </template>
    </div>

    <div class="text-caption text-medium-emphasis">
      Discover
      {{ countryState.title }} companies<template
        v-if="store.countryState.markets.length"
      >
        that are on the
        {{ countryState.markets[0]?.title }}</template
      >
      <template v-else> from around the world</template>.
    </div>
  </div>
</template>
