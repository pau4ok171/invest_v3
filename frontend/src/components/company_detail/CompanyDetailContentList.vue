<template>
<div class="detail__content-list">
  <article>

    <CompanyDetailSummary/>

    <CompanyDetailValuation/>

    <div class="detail__future"></div>

    <div class="detail__past"></div>

    <div class="detail__health"></div>

    <div class="detail__dividend"></div>

    <div class="detail__management"></div>

    <div class="detail__ownership"></div>

    <div class="detail__other"></div>

  </article>
</div>
</template>

<script lang="ts">
import CompanyDetailSummary from "@/components/company_detail/CompanyDetailSummary.vue";
import CompanyDetailValuation from "@/components/company_detail/CompanyDetailValuation.vue";

export default {
  name: 'CompanyDetailContentList',
  components: {
    CompanyDetailValuation,
    CompanyDetailSummary
  },
}
</script>

<style scoped>
.detail__content-list {
  position: relative;
  width: 100%;
  min-height: 0;
  flex: 0 0 75%;
  max-width: 75%;
}
</style>