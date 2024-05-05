<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyListInfo",
  computed: {
    ...mapGetters({
      active_filters: "companyList/getActiveFilters",
      list_updated: "companyList/getListUpdated",
    }),
  },
})
</script>

<template>
<section class="company-list__info">
  <div class="company-list__title">Largest {{ active_filters.country.title }} Stocks</div>
  <div class="company-list__updated"><span>Updated</span> {{ new Date(list_updated).toLocaleDateString('ru-RU') }}</div>
  <div class="company-list__description">
    Discover {{ active_filters.country.title }} companies<template v-if="active_filters.country.markets"> that are on the {{ active_filters.country.markets[0].title }}</template>.
  </div>
</section>
</template>

<style scoped>
.company-list__info {
  padding: 10px 0;
  display: grid;
  grid-row: 2 / auto;
}
.company-list__title {
  margin-bottom: 8px;
  font-size: 2.8rem;
  line-height: 1.25;
  font-weight: 500;
}
.company-list__updated {
  font-size: 1.2rem;
  line-height: 1.5;
}
.company-list__updated span {
  color: rgba(255, 255, 255, .7);
  text-transform: uppercase;
}
.company-list__description {
  margin-top: 16px;
  font-size: 1.4rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, .5);
}
</style>