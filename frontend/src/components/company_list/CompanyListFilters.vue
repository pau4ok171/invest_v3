<script lang="ts">
import {defineComponent} from 'vue'
import BaseButton from "@/components/UI/buttons/BaseButton.vue";
import FilterIcon from "@/components/icons/FilterIcon.vue";
import {mapGetters} from "vuex";
import TheCompanyListBasicFilter from "@/components/company_list/TheCompanyListBasicFilter.vue";

export default defineComponent({
  name: "CompanyListFilters",
  components: {
    TheCompanyListBasicFilter,
    FilterIcon,
    BaseButton
  },
  computed: {
    ...mapGetters({
      active_filters: "companyList/getActiveFilters",
      filters: "companyList/getFilters",
    }),
  },
})
</script>

<template>
<section class="company-list__filters">

  <div class="company-list__basic-filters">

    <TheCompanyListBasicFilter
        filter_name="country"
        :active_filter="active_filters.country"
        :filter="filters.country"
    />

    <TheCompanyListBasicFilter
        filter_name="sector"
        :active_filter="active_filters.sector"
        :filter="filters.sector"
    />

  </div>

  <div>
    <BaseButton>
      <span>Advanced filters</span>
      <FilterIcon/>
    </BaseButton>
  </div>

</section>
</template>

<style scoped>
.company-list__filters {
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: 40px;
  justify-content: space-between;
  align-items: center;
}
.company-list__basic-filters {
  display: grid;
  column-gap: 8px;
  grid-template-columns: auto auto;
}
</style>