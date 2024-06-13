<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import MultiplierVsPeersTabListDropDownMenu
  from "@/components/company_detail/content_list/valuation/MultiplierVsPeersTabListDropDownMenu.vue";
import RoundedBorderedButton from "@/components/UI/buttons/RoundedBorderedButton.vue";

export default defineComponent({
  name: "MultiplierVsPeersTabList",
  components: {
    RoundedBorderedButton,
    MultiplierVsPeersTabListDropDownMenu, DropDownMenuBox, ArrowDownIcon, RoundedButton}
})
</script>

<template>
<div class="detail-multiplier__tab-list">

  <div class="detail-multiplier__tab">
    <DropDownMenuBox>
      <template v-slot:button>
        <RoundedBorderedButton>
          <span>Default Peers</span>
          <ArrowDownIcon/>
        </RoundedBorderedButton>
      </template>
      <template v-slot:menu>
        <span class="chart__dropdown-menu"></span>
      </template>
    </DropDownMenuBox>
  </div>

  <div class="detail-multiplier__tab">

    <DropDownMenuBox>
      <template v-slot:button>
        <RoundedBorderedButton>
          <span>Price to Earnings</span>
          <ArrowDownIcon/>
        </RoundedBorderedButton>
      </template>
      <template v-slot:menu>
        <MultiplierVsPeersTabListDropDownMenu/>
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