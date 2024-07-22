<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import RoundedBorderedButton from "@/components/UI/buttons/RoundedBorderedButton.vue";
import type {Tab} from "@/components/company_detail/content_list/valuation/MultiplierVsPeers.vue";
import CompanyDetailMultiplierDropDownMenu
  from "@/components/company_detail/content_list/CompanyDetailMultiplierDropDownMenu.vue";

export default defineComponent({
  name: "MultiplierVsPeersTabList",
  components: {
    CompanyDetailMultiplierDropDownMenu,
    RoundedBorderedButton,
    DropDownMenuBox,
    ArrowDownIcon,
    RoundedButton
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

    <DropDownMenuBox>
      <template v-slot:button>
        <RoundedBorderedButton>
          <span>{{ get_mode_name }}</span>
          <ArrowDownIcon/>
        </RoundedBorderedButton>
      </template>
      <template v-slot:menu>
        <CompanyDetailMultiplierDropDownMenu @changeMode="(tab: Tab) => $emit('changeMode', tab)" :tabs/>
      </template>
    </DropDownMenuBox>

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