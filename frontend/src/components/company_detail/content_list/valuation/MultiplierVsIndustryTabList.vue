<script lang="ts">
import {defineComponent} from 'vue'
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import BaseButton from "@/components/UI/base/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "MultiplierVsIndustryTabList",
  components: {
    BaseButton,
    DropDownMenuBox,
  }
})
</script>

<template>
<div class="detail-multiplier__tab-list">

  <div class="detail-multiplier__tab">
    <DropDownMenuBox>
      <template v-slot:button>
        <base-button
          text="Price to Earnings"
          append-icon="ArrowDownIcon"
          variant="outlined"
          rounded="x-large"
          size="small"
          lower
        />
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