<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'

// Utilities
import { computed } from 'vue'

// Types
import type { CountryState } from '@/store/companyList/types'

const store = useCompanyListStore()
const countryState = computed<CountryState>(() => store.countryState)
</script>

<template>
  <section class="company-list__info">
    <div class="company-list__title">
      Largest {{ store.countryState.title }} Stocks
    </div>
    <div class="company-list__updated">
      <span>Updated </span>
      <v-skeleton-loader
        class="d-inline-block mt-n3 ml-n3"
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
    <div class="company-list__description">
      Discover
      {{ countryState.title }} companies<template
        v-if="store.countryState.markets.length"
      >
        that are on the
        {{ countryState.markets[0]?.title }}</template
      >
      <template v-else>
        from around the world
      </template>.
    </div>
  </section>
</template>

<style lang="scss">
.company-list__info {
  padding: 10px 0;
  display: grid;
  grid-row: 2 / auto;
}
.company-list__title {
  margin-bottom: 8px;
  font-size: 1.75rem;
  line-height: 1.25;
  font-weight: 500;
}
.company-list__updated {
  font-size: 0.75rem;
  line-height: 1.5;
}
.company-list__updated span {
  color: rgb(var(--v-theme-on-surface-variant));
  text-transform: uppercase;
}
.company-list__description {
  margin-top: 16px;
  font-size: 0.875rem;
  line-height: 1.5;
  color: rgb(var(--v-theme-on-surface-variant));
}
</style>
