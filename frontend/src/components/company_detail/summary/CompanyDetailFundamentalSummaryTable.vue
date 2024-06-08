<script lang="ts">
import {defineComponent} from 'vue'
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import QuestionText from "@/components/UI/text/QuestionText.vue";
import QuestionLink from "@/components/UI/text/QuestionLink.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailFundamentalSummaryTable",
  components: {QuestionLink, QuestionText, ArrowDownIcon},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_pe() {
      const marketCap = this.company.price_data.capitalisation
      const report = this.company.reports[0]
      if (!report || !marketCap) return 'n/a'

      const earnings = report.income_net
      const scale_unit = report.scale_unit
      return `${(earnings * scale_unit/marketCap).toFixed(1)}x`
    },
    get_pb() {
      const marketCap = this.company.price_data.capitalisation
      const report = this.company.reports[0]
      if (!report || !marketCap) return 'n/a'

      const bookValue = report.assets
      const scale_unit = report.scale_unit
      return `${(bookValue * scale_unit/marketCap).toFixed(1)}x`
    },
  }
})
</script>

<template>
<div class="detail-fundamental-summary-table">

  <div class="detail-fundamental-summary-table__in-row-item-box">
    <div class="detail-fundamental-summary-table__in-row-item">
      <h3 class="detail-fundamental-summary-table__title">{{ get_pe }}</h3>
      <span class="detail-fundamental-summary-table__text">P/E Ratio</span>
    </div>
    <div class="detail-fundamental-summary-table__in-row-item detail-fundamental-summary-table__flex-end">
      <div>
        <h3 class="detail-fundamental-summary-table__subtitle">{{ get_pb }}</h3>
        <span class="detail-fundamental-summary-table__subtext">P/B Ratio</span>
      </div>
    </div>
  </div>

  <div>
    <QuestionText>Is SBER overvalued?</QuestionText>
    <QuestionLink>See Fair Value and valuation analysis</QuestionLink>
  </div>

</div>
</template>

<style scoped>
.detail-fundamental-summary-table {
  margin-top: 50px;
}
.detail-fundamental-summary-table__in-row-item-box {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
.detail-fundamental-summary-table__in-row-item {
  padding-bottom: 24px;
  margin-top: 32px;
  max-width: 100%;
  flex: 0 0 50%;
}
.detail-fundamental-summary-table__flex-end {
  display: flex;
  align-items: flex-end;
}
.detail-fundamental-summary-table__title {
  font-size: 3.6rem;
  line-height: 1.25;
  font-weight: 500;
  margin-bottom: 2px;
}
.detail-fundamental-summary-table__subtitle {
  font-size: 2rem;
  line-height: 1.25;
  font-weight: 500;
  margin-bottom: 2px;
}
.detail-fundamental-summary-table__text {
  font-size: 1.6rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, .7);
}
.detail-fundamental-summary-table__subtext {
  font-size: 1.4rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, .7);
}
.detail-fundamental-summary-table__question {
  font-size: 1.6rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, .5);
  margin-top: 35px;
}
.detail-fundamental-summary-table__link {
  display: flex;
  font-size: 1.6rem;
  line-height: 1.5;
  font-weight: 500;
  color: var(--blue);
  text-decoration: underline;
}
.detail-fundamental-summary-table__link svg {
  transform: rotate(-90deg);
  margin-left: -6px;
  fill: var(--blue);
}
</style>