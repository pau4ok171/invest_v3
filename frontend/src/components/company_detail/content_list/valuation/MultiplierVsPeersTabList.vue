<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import type {Tab} from "@/components/company_detail/content_list/valuation/MultiplierVsPeers.vue";
import CompanyDetailMultiplierDropDownMenu
  from "@/components/company_detail/content_list/CompanyDetailMultiplierDropDownMenu.vue";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import BaseMenu from "@/components/UI/base/components/BaseMenu/BaseMenu.vue";

export default defineComponent({
  name: "MultiplierVsPeersTabList",
  components: {
    BaseMenu,
    BaseButton,
    CompanyDetailMultiplierDropDownMenu,
  },
  props: {
    tabs: {
      required: true,
      type: Object as PropType<{[p: string]: Tab}>
    },
  },
  computed: {
    get_mode_name() {
      return Object.values(this.tabs).find(t => t.active)?.name
    },
  },
})
</script>

<template>
<div class="detail-multiplier__tab-list">
  <div class="detail-multiplier__tab">

    <base-menu>
      <template v-slot:activator>
        <base-button
          :text="get_mode_name"
          append-icon="ArrowDownIcon"
          variant="outlined"
          rounded="x-large"
          size="small"
          lower
        />
      </template>
      <template v-slot:list>
        <CompanyDetailMultiplierDropDownMenu @changeMode="(tab: Tab) => $emit('changeMode', tab)" :tabs/>
      </template>
    </base-menu>

  </div>
</div>
</template>

<style scoped>
.detail-multiplier__tab-list {
  display: flex;
  justify-content: flex-end;
  gap: 4px;
  width: 100%;
  margin-bottom: 8px;
}
.detail-multiplier__tab {
  position: relative;
  display: inline-block;
}
</style>