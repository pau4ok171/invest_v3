<script setup lang="ts">
// Components
import FetchingData from '@/components/charts/FetchingData.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { ref } from 'vue'
import { chartOpts as _chartOpts } from '@/components/charts/multiplierVsPeersChart'

// Types
import type { PropType } from 'vue'
import type { MultiplierTab } from '@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue'

const props = defineProps({
  tabs: {
    required: true,
    type: Object as PropType<MultiplierTab[]>,
  },
})

const store = useCompanyDetailStore()

const chartOpts = ref(_chartOpts)
</script>

<template>
  <div class="detail-multiplier-vs-peers-chart">
    <fetching-data v-if="store.fetchingCompany" />
    <charts v-else :options="chartOpts" constructorType="chart" />
  </div>
</template>

<style lang="scss">
.detail-multiplier-vs-peers-chart svg {
  height: auto;
  width: auto;
}
.multiple-vs-peers-chart__v-axis-name {
  fill: rgb(255, 255, 255);
  border-bottom: 1px dotted rgb(35, 148, 223);
  width: fit-content;
  line-height: 16px;
  opacity: 0.7;
  font-size: 0.75rem;
}
.multiple-vs-peers-chart__middle-label-name {
  fill: #1b222d;
  font-size: 0.8125rem;
}
.multiple-vs-peers-chart__data-label-value {
  line-height: 1.5;
  font-weight: 500;
  color: #fff;
  font-size: 0.75rem;
}
.multiple-vs-peers-chart__data-label-name {
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.8);
  padding-right: 10px;
  font-weight: normal;
  font-size: 0.875rem;
}
.multiple-vs-peers-chart__data-label-name--selected {
  background: linear-gradient(
    270deg,
    rgb(35, 148, 223) 0%,
    rgb(35, 148, 223) 100%
  );
  padding: 0 6px;
  border-radius: 4px;
  margin-top: 2px;
  color: rgb(255, 255, 255);
}
</style>
