<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSnowflakeTable from "@/components/company_detail/summary/CompanyDetailSnowflakeTable.vue";
import SnowflakeChart from "@/components/charts/SnowflakeChart.vue";
import utils from "@/mixins/utils";

export default defineComponent({
  name: "TheCompanyDetailCompetitorsItem",
  components: {SnowflakeChart, CompanyDetailSnowflakeTable},
  props: {
    competitor: {
      type: Object,
      required: true,
    },
  },
  mixins: [utils],
})
</script>

<template>
<section class="detail-competitors__item">
<RouterLink class="detail-competitors__link" :to="competitor.absolute_url">
  <div class="detail-competitors__inner">
    <div class="competitors__snowflake">
      <CompanyDetailSnowflakeTable v-if="false"/>
      <SnowflakeChart v-else :chartData="Object.values(competitor.snowflake)" :isSmall="true"/>
    </div>

    <div class="detail-competitors__info">
      <p class="detail-competitors__info-text">{{ competitor.title }}</p>
      <p class="detail-competitors__info-text detail-competitors__info-text--medium">{{ competitor.market.title }}:{{ competitor.ticker }}</p>
      <p class="detail-competitors__info-text detail-competitors__info-text--medium detail-competitors__info-text--grey">
        {{ humanize_financial_val(competitor.price_data.capitalisation) }}
      </p>
    </div>
  </div>
</RouterLink>
</section>
</template>

<style scoped>
.detail-competitors__item {
    width: 164px;
    margin-right: 16px;
    text-align: center;
    border-radius: 8px;
    cursor: pointer;
    flex-shrink: 0;
  }
  .detail-competitors__item:hover {
    background-color: #262e3a;
  }
  .detail-competitors__inner {
    padding: 16px;
  }
  .detail-competitors__info {
    padding-right: 10px;
    margin-top: 8px;
  }
  .detail-competitors__info-text {
    font-size: 1.6rem;
    line-height: 1.5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .detail-competitors__info-text--medium {
    font-size: 1.4rem;
  }
  .detail-competitors__info-text--grey {
    color: rgba(255, 255, 255, .5);
  }
</style>