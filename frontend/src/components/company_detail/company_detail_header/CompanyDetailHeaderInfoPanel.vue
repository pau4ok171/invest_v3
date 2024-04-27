<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailHeaderInfoItem
  from "@/components/company_detail/company_detail_header/CompanyDetailHeaderInfoItem.vue";
import SmallPriceChart from "@/components/charts/SmallPriceChart.vue";
import TextButton from "@/components/UI/buttons/TextButton.vue";
import utils from "@/mixins/utils";
import {mapGetters, mapMutations, mapState} from "vuex";
import CompanyDetailAnalystsModalMenu
  from "@/components/company_detail/summary/analysts/CompanyDetailAnalystsModalMenu.vue";

export default defineComponent({
  name: "CompanyDetailHeaderInfoPanel",
  components: {CompanyDetailAnalystsModalMenu, TextButton, SmallPriceChart, CompanyDetailHeaderInfoItem},
  computed: {
    totalIdeas() {
      return this.company.analyst_ideas.length
    },
    ...mapState({
      company: state => state.companyDetail.company,
    }),
    ...mapGetters({
      analystsModalMenuIsOpen: 'companyDetail/getAnalystsModalMenuIsOpen',
    })
  },
  methods: {
    ...mapMutations({
      setAnalystsModalMenuIsOpen: 'companyDetail/setAnalystsModalMenuIsOpen',
    }),
  },
  mixins: [utils,],
})
</script>

<template>
  <div class="detail-header__info-panel">

    <CompanyDetailHeaderInfoItem>
      <template v-slot:title><p>Last price</p></template>
      <template v-slot:value><span>₽{{ this.company.price_data.last_price.toFixed(2) }}</span></template>
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailHeaderInfoItem>
      <template v-slot:title><p>Market cap</p></template>
      <template v-slot:value><span>
        {{ this.humanize_financial_val(this.company.price_data.capitalisation, company.formatting.primaryCurrencySymbol) }}
      </span></template>
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailHeaderInfoItem>
      <template v-slot:title><p>7D</p></template>
      <template v-slot:value>
        <span :class="[this.company.price_data.return_7d > 0 ? 'detail-header__success-color' : 'detail-header__error-color']">
          {{ this.company.price_data.return_7d.toFixed(2)}}%
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailHeaderInfoItem>
      <template v-slot:title><p>1Y</p></template>
      <template v-slot:value>
        <span :class="[this.company.price_data.return_1y > 0 ? 'detail-header__success-color' : 'detail-header__error-color']">
          {{ this.company.price_data.return_1y.toFixed(2)}}%
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <SmallPriceChart class="detail-header__info-item"/>

    <CompanyDetailHeaderInfoItem class="detail-header__info-item--nowrap">
      <template v-slot:title><p>Updated</p></template>
      <template v-slot:value>
        <span class="detail-header__info-item-value--small">
          <template v-if="company.reports.length">{{ this.company.reports[0].updated}}</template>
          <template v-else>n/a</template>
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailHeaderInfoItem class="detail-header__info-item--nowrap">
      <template v-slot:title><p>Data</p></template>
      <template v-slot:value>
        <span class="detail-header__info-item-value--small detail-header__info-item-value--on-row">
          <span>Financials Company</span>
          <template v-if="company.analyst_ideas">
            <span> + </span>
            <TextButton @click="setAnalystsModalMenuIsOpen(true)">{{ this.totalIdeas }} Analysts</TextButton>
          </template>
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailAnalystsModalMenu v-if="analystsModalMenuIsOpen"/>

  </div>
</template>

<style scoped>
  .detail-header__info-panel {
    padding-left: 76px;
    display: grid;
    grid-template: 52px / repeat(4, min-content) 2fr 1fr 1fr;
  }
</style>