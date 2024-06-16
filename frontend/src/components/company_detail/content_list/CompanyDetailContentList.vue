<script lang="ts">
import {defineAsyncComponent, defineComponent} from "vue";

export default defineComponent({
  name: 'CompanyDetailContentList',
  components: {
    CompanyDetailSummary: defineAsyncComponent(() =>
        import("@/components/company_detail/content_list/summary/CompanyDetailSummary.vue")),
    CompanyDetailValuation: defineAsyncComponent(() =>
        import("@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue")),
  },
})
</script>

<template>
<div class="detail__content-list">
<article>
  <CompanyDetailSummary id="overview" class="detail__summary section_observer"/>

  <template v-if="false">

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

  </template>

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