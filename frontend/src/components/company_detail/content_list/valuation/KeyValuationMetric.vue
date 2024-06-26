<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import KeyValuationMetricTabList from "@/components/company_detail/content_list/valuation/KeyValuationMetricTabList.vue";
import KeyValuationMetricChart from "@/components/charts/KeyValuationMetricChart.vue";
import KeyValuationMetricTable from "@/components/company_detail/content_list/valuation/KeyValuationMetricTable.vue";
import {mapGetters} from "vuex";
import FetchingData from "@/components/charts/FetchingData.vue";

export interface Tab {
  name: string,
  id: string,
  value: number,
  active: boolean,
  metric: string,
}

export default defineComponent({
  name: "KeyValuationMetric",
  components: {
    FetchingData,
    KeyValuationMetricTable,
    KeyValuationMetricChart,
    KeyValuationMetricTabList,
    DetailAnalysisDesc,
    DetailAnalysisTitle,
  },
  data() {
    return {
      tabs: {
        pe: {name: 'PE', id: 'pe', value: 1, active: true, metric: ``},
        pb: {name: 'PB', id: 'pb', value: 2, active: false, metric: ''},
        ps: {name: 'PS', id: 'ps', value: 3, active: false, metric: ''},
        others: {name: 'Others', id: 'others', value: 0, active: false, metric: 'Other financial metrics that can be useful for relative valuation'},
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
      return `Which metric is best to use when looking at relative valuation for ${this.company.slug.toUpperCase()}?`
    },
    get_tabs() {
      const tabs = {...this.tabs}
      if (this.company.slug) {
        const slug = this.company.slug.toUpperCase()
        tabs.pe.metric = `As ${slug} is profitable we use its Price-To-Earnings Ratio for relative valuation analysis`
        tabs.pb.metric = `For ${slug} we can also use its Price-To-Book Ratio for relative valuation analysis`
        tabs.ps.metric = `As ${slug} is a bank we don’t use its Price-To-Sales Ratio as the key metric for relative valuation analysis`
      }
      return tabs
    },
  },
  methods: {
    changeTab(tab: Tab) {
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
    <span>1.2</span>Key Valuation Metric
  </DetailAnalysisTitle>
  <DetailAnalysisDesc>
    {{ get_section_desc }}
  </DetailAnalysisDesc>

  <div class="detail__content">
    <div class="detail__content-item detail-key-valuation-metric">

      <KeyValuationMetricTabList @changeTab="changeTab" :tabs="get_tabs"/>

      <div class="detail-key-valuation-metric__chart-box">

        <KeyValuationMetricChart v-if="pageIsReady && !get_tabs.others.active" :tabs="get_tabs"/>
        <FetchingData style="height: 280px;" v-else-if="!pageIsReady"/>

        <KeyValuationMetricTable v-else/>

      </div>

    </div>
  </div>
</section>
</template>

<style scoped>
.detail-key-valuation-metric {
  display: grid;
  grid-template-columns: 35% auto;
  gap: 20px;
}
.detail-key-valuation-metric__chart-box {
  display: grid;
}
</style>