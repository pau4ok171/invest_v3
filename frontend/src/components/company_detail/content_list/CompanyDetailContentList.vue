<script setup lang="ts">
// Components
import CompanyDetailSummary from '@/components/company_detail/content_list/summary/CompanyDetailSummary.vue'
import CompanyDetailValuation from '@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue'
import CompanyDetailFuture from '@/components/company_detail/content_list/future/CompanyDetailFuture.vue'
import CompanyDetailPast from '@/components/company_detail/content_list/past/CompanyDetailPast.vue'
import CompanyDetailHealth from '@/components/company_detail/content_list/health/CompanyDetailHealth.vue'
import CompanyDetailDividend from '@/components/company_detail/content_list/dividend/CompanyDetailDividend.vue'

// Composables
import { useSectionContext } from '@/composables/sectionObserver'

// Utilities
import { onMounted } from 'vue'
import { SECTIONS } from '@/assets/static/companyDetail'

const { registerSection } = useSectionContext()

onMounted(() => {
  SECTIONS.forEach((section) => {
    const el = document.querySelector(`#${section.value}`)
    if (el) {
      registerSection(section.value, el)
    }
  })
})
</script>

<template>
  <div class="detail__content-list">
    <article>
      <company-detail-summary id="overview" />

      <company-detail-valuation id="valuation" />

      <company-detail-future id="future" />

      <company-detail-past id="past" />

      <company-detail-health id="health" />

      <company-detail-dividend id="dividend" />

      <template v-if="false">
        <div id="management"></div>
        <div class="detail__management"></div>

        <div id="ownership"></div>
        <div class="detail__ownership"></div>

        <div id="other"></div>
        <div class="detail__other"></div>
      </template>
    </article>
  </div>
</template>

<style lang="scss" scoped>
@use 'vuetify/settings' as vuetify;

.detail__content-list {
  position: relative;
  width: 100%;
  min-height: 0;
  flex: 0 0 75%;
  max-width: 75%;

  @media #{map-get(vuetify.$display-breakpoints, 'lg-and-down')} {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>
