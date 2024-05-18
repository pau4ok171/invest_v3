<script lang="ts">
import {defineComponent} from 'vue'
import QuestionText from "@/components/UI/text/QuestionText.vue";
import QuestionLink from "@/components/UI/text/QuestionLink.vue";

export default defineComponent({
  name: "CompanyDetailDividendsTable",
  components: {
    QuestionLink,
    QuestionText,
  }
})
</script>

<template>
<div>
  <div class="detail-dividends-table">
    <div class="detail-dividends-table__item">
      <h3 class="detail-dividends-table__title">14.0%</h3>
      <span class="detail-dividends-table__text">Current Dividend Yield</span>
    </div>
    <div class="detail-dividends-table__item">
      <h3 class="detail-dividends-table__title">35%</h3>
      <span class="detail-dividends-table__text">Payout Ratio</span>
    </div>
  </div>
  <div>
    <QuestionText>Does SBER pay a reliable dividends?</QuestionText>
    <QuestionLink>See SBER dividend history and benchmarks</QuestionLink>
  </div>
</div>
</template>

<style scoped>
  .detail-dividends-table {
    display: flex;
    flex-flow: wrap;
    justify-content: left;
  }
  .detail-dividends-table__item {
    max-width: 100%;
    flex: 0 0 50%;
  }
  .detail-dividends-table__title {
    font-size: 2rem;
    line-height: 1.25;
    font-weight: 500;
    margin-top: 24px;
    margin-bottom: 2px;
  }
  .detail-dividends-table__text {
    font-size: 1.6rem;
    line-height: 1.5;
    font-weight: 500;
    color: rgba(255, 255, 255, .7);
  }
</style>