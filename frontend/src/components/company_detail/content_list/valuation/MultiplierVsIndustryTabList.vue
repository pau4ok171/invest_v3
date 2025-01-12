<script lang="ts">
import {defineComponent} from 'vue'
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseMenu from "@/apps/visagiste/components/BaseMenu/BaseMenu.vue";

export default defineComponent({
  name: "MultiplierVsIndustryTabList",
  components: {
    BaseMenu,
    BaseButton,
  }
})
</script>

<template>
<div class="detail-multiplier__tab-list">

  <div class="detail-multiplier__tab">
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