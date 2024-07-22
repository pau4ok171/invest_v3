<script lang="ts">
import {defineComponent} from 'vue'
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import RoundedBorderedButton from "@/components/UI/buttons/RoundedBorderedButton.vue";

export default defineComponent({
  name: "MultiplierVsIndustryTabList",
  components: {
    RoundedBorderedButton,
    DropDownMenuBox,
    ArrowDownIcon,
  }
})
</script>

<template>
<div class="detail-multiplier__tab-list">

  <div class="detail-multiplier__tab">
    <DropDownMenuBox>
      <template v-slot:button>
        <RoundedBorderedButton>
          <span>Price to Earnings</span>
          <ArrowDownIcon/>
        </RoundedBorderedButton>
      </template>
      <template v-slot:menu>
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