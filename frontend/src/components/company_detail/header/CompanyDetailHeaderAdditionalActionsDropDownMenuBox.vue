<script lang="ts">
import {defineComponent} from 'vue'
import TheCompanyDetailHeaderMoreDropDownMenu
  from "@/components/company_detail/header/TheCompanyDetailHeaderMoreDropDownMenu.vue";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import BaseMenu from "@/components/UI/base/components/BaseMenu/BaseMenu.vue";

export default defineComponent({
  name: "CompanyDetailHeaderAdditionalActionsDropDownMenuBox",
  components: {
    BaseMenu,
    BaseButton,
    TheCompanyDetailHeaderMoreDropDownMenu
  }
})
</script>

<template>
<base-menu>
  <template #activator>
    <base-button
      :icon="{value: 'DotsIcon', size: 'large'}"
      color="#000"
      rounded="x-small"
      density="compact"
    />
  </template>
  <template #list>
    <TheCompanyDetailHeaderMoreDropDownMenu/>
  </template>
</base-menu>
</template>
