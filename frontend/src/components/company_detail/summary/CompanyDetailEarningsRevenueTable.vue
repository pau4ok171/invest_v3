<script lang="ts">
import {defineComponent} from 'vue'
import QuestionText from "@/components/UI/text/QuestionText.vue";
import QuestionLink from "@/components/UI/text/QuestionLink.vue";

export default defineComponent({
  name: "CompanyDetailEarningsRevenueTable",
  components: {QuestionLink, QuestionText}
})
</script>

<template>
<section class="detail-earnings-revenue-table__box">
  <div class="detail-earnings-revenue-table__item">
    <p class="detail-earnings-revenue-table__title">Last Reported Earnings</p>
    <p class="detail-earnings-revenue-table__text">Dec 31, 2021</p>
  </div>
  <div class="detail-earnings-revenue-table__item">
    <p class="detail-earnings-revenue-table__title">Next Earnings</p>
    <p class="detail-earnings-revenue-table__text">n/a</p>
  </div>

  <table class="detail-earnings-revenue-table table">
    <tbody>
      <tr>
        <td><span>Earnings per share (EPS)</span></td>
        <td>51.56</td>
      </tr>
      <tr>
        <td><span>Gross Margin</span></td>
        <td>98.05%</td>
      </tr>
      <tr>
        <td><span>Net Profit Margin</span></td>
        <td>47.64%</td>
      </tr>
      <tr>
        <td><span>Debt/Equity Ratio</span></td>
        <td>90.3%</td>
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