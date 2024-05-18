<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from "vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import CompanyListFilterDropDownMenu from "@/components/company_list/CompanyListFilterDropDownMenu.vue";
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default defineComponent({
  name: "TheCompanyListBasicFilter",
  components: {
    RoundedButton,
    CompanyListFilterDropDownMenu,
    ArrowDownIcon,
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
      <RoundedButton>
        <span>{{ active_filter.title }}</span>
        <ArrowDownIcon/>
      </RoundedButton>
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