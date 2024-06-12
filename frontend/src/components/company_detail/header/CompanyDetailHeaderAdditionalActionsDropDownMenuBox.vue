<script lang="ts">
import {defineComponent} from 'vue'
import TheCompanyDetailHeaderMoreDropDownMenu
  from "@/components/company_detail/header/TheCompanyDetailHeaderMoreDropDownMenu.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
import DotsIcon from "@/components/icons/DotsIcon.vue";

export default defineComponent({
  name: "CompanyDetailHeaderAdditionalActionsDropDownMenuBox",
  components: {DotsIcon, RoundedWhiteButton, DropDownMenuBox, TheCompanyDetailHeaderMoreDropDownMenu}
})
</script>

<template>
<DropDownMenuBox>
  <template #button>
    <RoundedWhiteButton><DotsIcon/></RoundedWhiteButton>
  </template>
  <template #menu>
    <TheCompanyDetailHeaderMoreDropDownMenu/>
  </template>
</DropDownMenuBox>
</template>
