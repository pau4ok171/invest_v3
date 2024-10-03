<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from "vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import CompanyListFilterDropDownMenu from "@/components/company_list/CompanyListFilterDropDownMenu.vue";
import BaseButton from "@/components/UI/base/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "TheCompanyListBasicFilter",
  components: {
    BaseButton,
    CompanyListFilterDropDownMenu,
    DropDownMenuBox
  },
  props: {
    active_filter: {
      type: Object as PropType<any>,
      required: true,
    },
    filter: {
      type: Array,
      required: true,
    },
    filter_name: {
      type: String,
      required: true,
    },
    has_search: {
      type: Boolean,
      default: true
    }
  },
})
</script>

<template>
<div class="company-list__basic-filter">
  <DropDownMenuBox>
    <template v-slot:button>
      <base-button
        :text="active_filter.title"
        append-icon="ArrowDownIcon"
        variant="outlined"
      />
    </template>
    <template v-slot:menu>
      <CompanyListFilterDropDownMenu
          :filter
          :active_filter
          :has_search
          :filter_name
      />
    </template>
  </DropDownMenuBox>
</div>
</template>

<style scoped>
.company-list__basic-filter {
  position: relative;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, .2);
}
</style>