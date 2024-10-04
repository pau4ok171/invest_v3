<script lang="ts">
import {defineComponent} from 'vue'
import TheCompanyDetailHeaderMoreDropDownMenu
  from "@/components/company_detail/header/TheCompanyDetailHeaderMoreDropDownMenu.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import BaseButton from "@/components/UI/base/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailHeaderAdditionalActionsDropDownMenuBox",
  components: {BaseButton, DropDownMenuBox, TheCompanyDetailHeaderMoreDropDownMenu}
})
</script>

<template>
<DropDownMenuBox>
  <template #button>
    <base-button
      :icon="{value: 'DotsIcon', size: 'large'}"
      color="#000"
      rounded="x-small"
      density="compact"
    />
  </template>
  <template #menu>
    <TheCompanyDetailHeaderMoreDropDownMenu/>
  </template>
</DropDownMenuBox>
</template>
