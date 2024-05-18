<script lang="ts">
import CompanyListInfo from "@/components/company_list/CompanyListInfo.vue";
import CompanyListFilters from "@/components/company_list/CompanyListFilters.vue";
import CompanyListOptions from "@/components/company_list/CompanyListOptions.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: "CompanyListHeader",
  components: {
    CompanyListOptions,
    CompanyListFilters,
    CompanyListInfo,
 },
})
</script>

<template>
<header class="company-list__header">

  <CompanyListInfo/>

  <CompanyListFilters/>

  <CompanyListOptions/>

</header>
</template>

<style scoped>
.company-list__header {
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, .1);
  display: grid;
}
</style>