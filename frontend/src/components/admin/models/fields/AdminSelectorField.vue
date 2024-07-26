<script lang="ts">
import {defineComponent} from 'vue'
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import BaseInput from "@/components/UI/base/BaseInput.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import CompanyListFilterDropDownMenu from "@/components/company_list/CompanyListFilterDropDownMenu.vue";
import AdminSelectorDropDownMenu from "@/components/admin/models/fields/AdminSelectorDropDownMenu.vue";
import type {SelectorOption} from "@/types/admin";

export default defineComponent({
  name: "AdminSelectorField",
  components: {
    AdminSelectorDropDownMenu,
    CompanyListFilterDropDownMenu,
    RoundedButton,
    DropDownMenuBox,
    ArrowDownIcon,
    BaseInput,
    CheckedIcon
  },
  data() {
    return {
      activeOption: {name: '', slug: ''} as SelectorOption,
    }
  },
  props: {
    hasSearch: {
      type: Boolean,
      default: false,
    },
    options: {
      type: Array<SelectorOption>,
      required: true,
    },
    label: {
      type: String,
      default: 'Label',
    },
    helpText: {
      type: String
    },
    isRequired: {
      type: Boolean,
      default: false,
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    activeOption: {
      handler(option: SelectorOption) {
        this.$emit('changeOption', option)
      },
      deep: true
    },
  },

})
</script>

<template>
<DropDownMenuBox>
  <template v-slot:button>
    <RoundedButton>
      <span>{{ activeOption.name }}</span>
      <ArrowDownIcon/>
    </RoundedButton>
  </template>
  <template v-slot:menu>
    <AdminSelectorDropDownMenu
        v-model:activeOption="activeOption"
        :options
        :hasSearch
    />
  </template>
</DropDownMenuBox>
</template>

<style scoped>

</style>