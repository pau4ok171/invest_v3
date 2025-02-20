<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import MultiplierVsPeersTabList from "@/components/company_detail/content_list/valuation/MultiplierVsPeersTabList.vue";
import MultiplierVsPeersChart from "@/components/charts/MultiplierVsPeersChart.vue";
import CompanyDetailCheck from "@/components/company_detail/content_list/CompanyDetailCheck.vue";
import {mapGetters} from "vuex";
import FetchingData from "@/components/charts/FetchingData.vue";

export interface Tab {
  name: string,
  short_name: string,
  id: string,
  value: number,
  active: boolean,
}

export default defineComponent({
  name: "MultiplierVsPeers",
  components: {
    FetchingData,
    CompanyDetailCheck,
    MultiplierVsPeersChart,
    MultiplierVsPeersTabList,
    DetailAnalysisDesc,
    DetailAnalysisTitle
  },
  data() {
    return {
      tabs: {
        pe: {name: 'Price to Earnings', short_name: 'PE', id: 'price_to_earnings', value: 1, active: true,},
        pb: {name: 'Price to Book', short_name: 'PB', id: 'price_to_book', value: 2, active: false,},
        ps: {name: 'Price to Sales', short_name: 'PS', id: 'price_to_sales', value: 3, active: false,},
      } as {[p: string]: Tab}
    }
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      pageIsReady: 'companyDetail/getPageIsReady',
    }),
    get_section_desc() {
      if (!this.company.slug) return ''
      const short_name = Object.values(this.tabs).find(t => t.active)?.short_name.toUpperCase() || ''
      return `How does ${this.company.slug.toUpperCase()}'s ${short_name} Ratio compare to its peers?`
    },
  },
  methods: {
    changeMode(tab: Tab) {
      // Во всех tabs поставить режим false
      Object.values(this.tabs).forEach(tab => tab.active = false)
      // Активировать нажатый таб
      const clicked_tab = Object.values(this.tabs).find(t => t.id === tab.id)
      if (clicked_tab) clicked_tab.active = true
    }
  },
})
</script>

<template>
<section>

  <DetailAnalysisTitle>
    <span>1.3</span>Price to Earnings Ratio vs Peers
  </DetailAnalysisTitle>

  <DetailAnalysisDesc>
    {{ get_section_desc }}
  </DetailAnalysisDesc>

  <div class="detail__content">
    <div class="detail__content-item">

      <MultiplierVsPeersTabList @changeMode="changeMode" :tabs/>
      <MultiplierVsPeersChart v-if="pageIsReady" :tabs/>
      <FetchingData style="height: 362px" v-else/>

    </div>

    <div class="detail__content-item detail__point-list">
      <CompanyDetailCheck name="IsGoodValueComparingPriceToEarningsToPeersAverageValue"/>
    </div>

  </div>

</section>
</template>
