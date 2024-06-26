<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import {mapGetters} from "vuex";
import type {Tab} from "@/components/company_detail/content_list/valuation/KeyValuationMetric.vue";

export default defineComponent({
  name: "KeyValuationMetricTabList",
  components: {
    SolidStarIcon
  },
  props: {
    tabs: {
      type: Object as PropType<{[p: string]: Tab}>,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_key_metric() {
      return Object.values(this.tabs).find(t => t.active)?.metric
    }
  },
})
</script>

<template>
<div class="detail-key-valuation-metric__tab-list">
  <div role="tablist" class="detail-key-valuation-metric__tab-button-list">

    <button
      role="tab"
      class="detail-key-valuation-metric__tab-button"
      v-for="tab in tabs"
      :key="tab.id"
      :disabled="tab.active"
      @click="$emit('changeTab', tab)"
    >
      {{ tab.name }}
    </button>

  </div>
  <div class="detail-key-valuation-metric__tab-desc">

    <div class="detail-key-valuation-metric__tab-icon">
      <SolidStarIcon/>
    </div>

    <div class="detail-key-valuation-metric__text">
      <p class="detail-key-valuation-metric__text-desc">
        <mark class="detail-key-valuation-metric__text-mark">Key metric: </mark>
        <span>{{ get_key_metric }}</span>
      </p>
    </div>

  </div>
</div>
</template>

<style scoped>
.detail-key-valuation-metric__tab-list {
  display: grid;
  align-content: start;
}
.detail-key-valuation-metric__tab-button-list {
  display: grid;
  grid-template-columns: repeat(4, auto);
}
.detail-key-valuation-metric__tab-button {
  display: block;
  width: 100%;
  height: auto;
  border-top: 1px solid transparent;
  border-left: 1px solid transparent;
  border-right: 1px solid transparent;
  padding: 4px;
  font-size: 1.4rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, .3);
  border-radius: 4px;
}
.detail-key-valuation-metric__tab-button:disabled {
  color: rgb(255, 255, 255);
  background-color: rgba(0, 0, 0, .3);
  cursor: auto;
}
.detail-key-valuation-metric__tab-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}
.detail-key-valuation-metric__tab-desc {
  display: grid;
  grid-template-columns: 30px auto;
  grid-template-rows: auto;
  background-color: rgb(38, 46, 58);
  gap: 10px;
  padding: 10px;
  border-radius: 4px;
  height: min-content;
  margin-top: 16px;
}
.detail-key-valuation-metric__tab-icon {
  display: grid;
  justify-content: center;
}
.detail-key-valuation-metric__tab-icon svg {
  fill: var(--blue);
}
.detail-key-valuation-metric__text {
  display: grid;
}
.detail-key-valuation-metric__text-desc {
  line-height: 1.5;
  font-size: 1.4rem;
}
.detail-key-valuation-metric__text-mark {
  background-color: transparent;
  color: var(--blue);
}
</style>