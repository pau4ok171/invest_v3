<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailHeaderInfoItem
  from "@/components/company_detail/header/CompanyDetailHeaderInfoItem.vue";
import SmallPriceChart from "@/components/charts/SmallPriceChart.vue";
import utils from "@/mixins/utils";
import {mapGetters} from "vuex";
import CompanyDetailHeaderAnalystsButtonModalMenuContainer
  from "@/components/company_detail/header/CompanyDetailHeaderAnalystModalMenuContainer.vue";

export default defineComponent({
  name: "CompanyDetailHeaderInfoPanel",
  components: {
    CompanyDetailHeaderAnalystsButtonModalMenuContainer,
    SmallPriceChart,
    CompanyDetailHeaderInfoItem
  },
  computed: {
    totalIdeas() {
      return this.company.analyst_ideas.length
    },
    ...mapGetters({
      company: "companyDetail/getCompany",
    }),
  },
  mixins: [utils,],
})
</script>

<template>
<div class="detail-header__info-panel" v-if="company.price_data">

  <CompanyDetailHeaderInfoItem>
    <template v-slot:title><p>Last price</p></template>
    <template v-slot:value><span>{{ company.formatting.primaryCurrencySymbol }}{{ company.price_data.last_price.toFixed(2) }}</span></template>
  </CompanyDetailHeaderInfoItem>

  <CompanyDetailHeaderInfoItem>
    <template v-slot:title><p>Market cap</p></template>
    <template v-slot:value><span>
      {{ humanize_financial_val(company.price_data.capitalisation, company.formatting.primaryCurrencySymbol) }}
    </span></template>
  </CompanyDetailHeaderInfoItem>

  <CompanyDetailHeaderInfoItem>
    <template v-slot:title><p>7D</p></template>
    <template v-slot:value>
      <span :class="[company.return_7d > 0 ? 'detail-header__success-color' : 'detail-header__error-color']">
        {{ company.return_7d.toFixed(2)}}%
      </span>
    </template>
  </CompanyDetailHeaderInfoItem>

  <CompanyDetailHeaderInfoItem>
    <template v-slot:title><p>1Y</p></template>
    <template v-slot:value>
      <span :class="[company.return_1y > 0 ? 'detail-header__success-color' : 'detail-header__error-color']">
        {{ company.return_1y.toFixed(2)}}%
      </span>
    </template>
  </CompanyDetailHeaderInfoItem>

  <SmallPriceChart class="detail-header__info-item"/>

  <CompanyDetailHeaderInfoItem class="detail-header__info-item--nowrap">
    <template v-slot:title><p>Updated</p></template>
    <template v-slot:value>
      <span class="detail-header__info-item-value--small">
        <template v-if="company.reports.length">{{ company.reports[0].updated}}</template>
        <template v-else>n/a</template>
      </span>
    </template>
  </CompanyDetailHeaderInfoItem>

  <CompanyDetailHeaderInfoItem class="detail-header__info-item--nowrap">
    <template v-slot:title><p>Data</p></template>
    <template v-slot:value>
      <span class="detail-header__info-item-value--small detail-header__info-item-value--on-row detail-header__info-panel-total-ideas">
        <span>Financials Company</span>
        <template v-if="!!totalIdeas">
          <span> + </span>
         <CompanyDetailHeaderAnalystsButtonModalMenuContainer/>
        </template>
      </span>
    </template>
  </CompanyDetailHeaderInfoItem>

</div>
</template>

<style scoped>
.detail-header__info-panel {
  padding-left: 76px;
  display: grid;
  grid-template: 52px / repeat(4, min-content) 2fr 1fr 1fr;
}
.detail-header__info-panel-total-ideas {
  align-items: flex-end;
}
</style>