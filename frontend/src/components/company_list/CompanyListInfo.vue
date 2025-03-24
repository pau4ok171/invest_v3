<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList'
import BaseSkeletonLoader from '@/apps/visagiste/components/BaseSkeletonLoader/BaseSkeletonLoader.vue'

const companyListStore = useCompanyListStore()
</script>

<template>
  <section class="company-list__info">
    <div class="company-list__title">
      Largest {{ companyListStore.activeFilters.country.title }} Stocks
    </div>
    <div class="company-list__updated">
      <span>Updated </span>
      <base-skeleton-loader
        class="d-inline-block mt-n3 ml-n3"
        v-if="companyListStore.fetching"
        width="120"
        type="text"
      />
      <template v-else>
        {{
          companyListStore.lastUpdate
            ? new Date(companyListStore.lastUpdate).toLocaleDateString('ru-RU')
            : 'n/a'
        }}
      </template>
    </div>
    <div class="company-list__description">
      Discover
      {{ companyListStore.activeFilters.country.title }} companies<template
        v-if="companyListStore.activeFilters.country.markets"
      >
        that are on the
        {{ companyListStore.activeFilters.country.markets[0]?.title }}</template
      >.
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
  color: rgb(var(--base-theme-on-surface-variant));
  text-transform: uppercase;
}
.company-list__description {
  margin-top: 16px;
  font-size: 0.875rem;
  line-height: 1.5;
  color: rgb(var(--base-theme-on-surface-variant));
}
</style>
