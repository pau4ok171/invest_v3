<script lang="ts">
import CompanyDetailSummary from "@/components/company_detail/content_list/summary/CompanyDetailSummary.vue";
import CompanyDetailValuation from "@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'CompanyDetailContentList',
  components: {
    CompanyDetailValuation,
    CompanyDetailSummary
  },
})
</script>

<template>
<div class="detail__content-list">
<article>
  <CompanyDetailSummary id="overview" class="detail__summary section_observer"/>

  <CompanyDetailValuation id="value" class="section_observer"/>

  <div id="future" class="section_observer"></div>
  <div class="detail__future"></div>

  <div id="past" class="section_observer"></div>
  <div class="detail__past"></div>

  <div id="health" class="section_observer"></div>
  <div class="detail__health"></div>

  <div id="dividend" class="section_observer"></div>
  <div class="detail__dividend"></div>

  <div id="management" class="section_observer"></div>
  <div class="detail__management"></div>

  <div id="owners" class="section_observer"></div>
  <div class="detail__ownership"></div>

  <div id="other" class="section_observer"></div>
  <div class="detail__other"></div>

</article>
</div>
</template>

<style scoped>
.detail__content-list {
  position: relative;
  width: 100%;
  min-height: 0;
  flex: 0 0 75%;
  max-width: 75%;
}
</style>