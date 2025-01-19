<script lang="ts">
import {defineComponent} from "vue";
import CompanyListInfo from "@/components/company_list/CompanyListInfo.vue";
import CompanyListFilters from "@/components/company_list/CompanyListFilters.vue";
import CompanyListOptions from "@/components/company_list/CompanyListOptions.vue";

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
<section class="company-list__header">

  <CompanyListInfo/>

  <CompanyListFilters/>

  <CompanyListOptions/>

</section>
</template>

<style lang="scss">
.company-list__header {
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(var(--base-theme-on-background), var(--base-border-opacity));
  display: grid;
}
</style>