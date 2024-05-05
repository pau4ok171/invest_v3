<template>
  <header class="company-list__header">

    <CompanyListInfo/>

    <CompanyListFilters/>

    <CompanyListOptions/>

  </header>
</template>

<script lang="ts">
import CompanyListInfo from "@/components/company_list/CompanyListInfo.vue";
import CompanyListFilters from "@/components/company_list/CompanyListFilters.vue";
import CompanyListOptions from "@/components/company_list/CompanyListOptions.vue";

export default {
  name: "CompanyListHeader",
  components: {
    CompanyListOptions,
    CompanyListFilters,
    CompanyListInfo,
  },
}
</script>

<style scoped>
.company-list__header {
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, .1);
  display: grid;
}
</style>