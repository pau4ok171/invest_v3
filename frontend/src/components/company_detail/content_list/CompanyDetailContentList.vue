<script setup lang="ts">
// Components
import CompanyDetailSummary from '@/components/company_detail/content_list/summary/CompanyDetailSummary.vue'
import CompanyDetailValuation from '@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue'
import CompanyDetailFuture from '@/components/company_detail/content_list/future/CompanyDetailFuture.vue'
import CompanyDetailPast from '@/components/company_detail/content_list/past/CompanyDetailPast.vue'
import CompanyDetailHealth from '@/components/company_detail/content_list/health/CompanyDetailHealth.vue'
import CompanyDetailDividend from '@/components/company_detail/content_list/dividend/CompanyDetailDividend.vue'
</script>

<template>
  <div class="detail__content-list">
    <article>
      <company-detail-summary
        id="overview"
        class="detail__summary section_observer"
      />

      <company-detail-valuation id="value" class="section_observer" />

      <company-detail-future id="future" class="section_observer" />

      <company-detail-past id="past" class="section_observer" />

      <company-detail-health id="health" class="section_observer" />

      <company-detail-dividend id="dividend" class="section_observer" />

      <template v-if="false">
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
