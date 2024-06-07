<script lang="ts">
import {defineComponent} from 'vue'
import QuestionText from "@/components/UI/text/QuestionText.vue";
import QuestionLink from "@/components/UI/text/QuestionLink.vue";
import {mapGetters} from "vuex";
import {DateTime} from "luxon";
import type {Report} from "@/types/invest";

export default defineComponent({
  name: "CompanyDetailEarningsRevenueTable",
  components: {QuestionLink, QuestionText},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_last_earnings() {
      if (this.company.last_reported_earnings) {
        return DateTime.fromISO(this.company.last_reported_earnings).toFormat('LLL dd, yyyy')
      }
      return 'n/a'
    },
    get_next_earnings() {
      if (this.company.next_earnings) {
        return DateTime.fromISO(this.company.next_earnings).toFormat('LLL dd, yyyy')
      }
      return 'n/a'
    },
    get_eps() {
      const report: Report = this.company.reports[0]
      if (!report) return 'n/a'
      return (report.income_net * report.scale_unit / report.share_outstanding).toFixed(2)
    },
    get_gross_margin() {
      const report: Report = this.company.reports[0]
      if (!report) return 'n/a'
      return `${(report.gross_margin / report.sales * 100).toFixed(2)}%`
    },
    get_net_profit_margin() {
      const report: Report = this.company.reports[0]
      if (!report) return 'n/a'
      return `${(report.income_net / report.sales * 100).toFixed(2)}%`
    },
    get_debt_equity_ratio() {
      const report: Report = this.company.reports[0]
      if (!report) return 'n/a'
      return `${(report.debt / report.equity * 100).toFixed(2)}%`
    },
  },
})
</script>

<template>
<section class="detail-earnings-revenue-table__box">
  <div class="detail-earnings-revenue-table__item">
    <p class="detail-earnings-revenue-table__title">Last Reported Earnings</p>
    <p class="detail-earnings-revenue-table__text">{{ get_last_earnings }}</p>
  </div>
  <div class="detail-earnings-revenue-table__item">
    <p class="detail-earnings-revenue-table__title">Next Earnings</p>
    <p class="detail-earnings-revenue-table__text">{{ get_next_earnings }}</p>
  </div>

  <table class="detail-earnings-revenue-table table">
    <tbody>
      <tr>
        <td><span>Earnings per share (EPS)</span></td>
        <td>{{ get_eps }}</td>
      </tr>
      <tr>
        <td><span>Gross Margin</span></td>
        <td>{{ get_gross_margin }}</td>
      </tr>
      <tr>
        <td><span>Net Profit Margin</span></td>
        <td>{{ get_net_profit_margin }}</td>
      </tr>
      <tr>
        <td><span>Debt/Equity Ratio</span></td>
        <td>{{ get_debt_equity_ratio }}</td>
      </tr>
    </tbody>
  </table>

  <QuestionText>How did SBER perform over the long term?</QuestionText>
  <QuestionLink>See historical performance and comparison</QuestionLink>

</section>
</template>

<style scoped>
.detail-earnings-revenue-table {
  font-size: 1.6rem;
  line-height: 1.5;
  margin-top: 32px;
}
.detail-earnings-revenue-table td {
  height: 38px;
  vertical-align: bottom;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, .1);
}
.detail-earnings-revenue-table td:first-child {
  color: rgba(255, 255, 255, .7);
}
.detail-earnings-revenue-table td:last-child {
  text-align: right;
}
.detail-earnings-revenue-table__box {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
.detail-earnings-revenue-table__item {
  max-width: 100%;
  flex: 0 0 50%;
}
.detail-earnings-revenue-table__title {
  font-size: 1.4rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, .5);
}
.detail-earnings-revenue-table__text {
  font-size: 1.4rem;
  line-height: 1.5;
}
</style>