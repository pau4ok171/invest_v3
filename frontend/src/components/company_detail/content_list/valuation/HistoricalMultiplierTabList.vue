<script lang="ts">
import {defineComponent} from 'vue'
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseMenu from "@/apps/visagiste/components/BaseMenu/BaseMenu.vue";

export default defineComponent({
  name: "HistoricalMultiplierTabList",
  components: {
    BaseMenu,
    BaseButton,
  }
})
</script>

<template>
<div class="detail-historical-multiplier-chart__tab-list-wrapper">

  <div class="detail-historical-multiplier-chart__tab-list">
    <div class="detail-historical-multiplier-chart__tab">
      <base-menu>
        <template v-slot:activator>
          <base-button
            text="Price to Earnings"
            append-icon="ArrowDownIcon"
            variant="outlined"
            rounded="x-large"
            size="small"
            lower
          />
        </template>

        <template v-slot:list>
        </template>
      </base-menu>
    </div>
  </div>

  <div class="detail-historical-multiplier-chart__period-tab-list">
    <div role="tablist" class="detail-historical-multiplier-chart__tab-list-inner">

      <button role="tab" value="3M" id="3M-tab" class="detail-historical-multiplier-chart__period-tab" disabled>3M</button>
      <button role="tab" value="1Y" id="1Y-tab" class="detail-historical-multiplier-chart__period-tab">1Y</button>
      <button role="tab" value="3Y" id="3Y-tab" class="detail-historical-multiplier-chart__period-tab">3Y</button>
      <button role="tab" value="5Y" id="5Y-tab" class="detail-historical-multiplier-chart__period-tab">5Y</button>

    </div>
  </div>

</div>
</template>

<style scoped>
.detail-historical-multiplier-chart__tab-list-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 8px 16px;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, .03);
  margin-bottom: 16px;
}
.detail-historical-multiplier-chart__tab-list {
  justify-self: start;
}
.detail-historical-multiplier-chart__tab {
  position: relative;
  display: inline-block;
}
.detail-historical-multiplier-chart__period-tab-list {
  justify-self: end;
}
.detail-historical-multiplier-chart__tab-list-inner {
  display: grid;
  grid-template-columns: repeat(4, 40px);
}
.detail-historical-multiplier-chart__period-tab {
  width: 100%;
  height: auto;
  border-top: 1px solid transparent;
  border-left: 1px solid transparent;
  border-right: 1px solid transparent;
  padding: 4px;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, .3);
  border-radius: 4px;
  font-size: 1.4rem;
}
.detail-historical-multiplier-chart__period-tab:disabled {
  cursor: auto;
  color: rgb(255, 255, 255);
  background-color: rgba(0, 0, 0, .3);
}
.detail-historical-multiplier-chart__period-tab:hover:not(:disabled) {
  background: rgba(255, 255, 255, .1);
}
</style>