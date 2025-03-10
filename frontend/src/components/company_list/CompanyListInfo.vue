<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'CompanyListInfo',
  computed: {
    ...mapGetters({
      active_filters: 'companyList/getActiveFilters',
      list_updated: 'companyList/getListUpdated',
    }),
  },
})
</script>

<template>
  <section class="company-list__info">
    <div class="company-list__title">
      Largest {{ active_filters.country.title }} Stocks
    </div>
    <div class="company-list__updated">
      <span>Updated</span>
      {{ new Date(list_updated).toLocaleDateString('ru-RU') }}
    </div>
    <div class="company-list__description">
      Discover {{ active_filters.country.title }} companies<template
        v-if="active_filters.country.markets"
      >
        that are on the {{ active_filters.country.markets[0].title }}</template
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
