<template>
  <CompanyListButton
      @click="this.isActive=!this.isActive"
      :class="{'company-list__button--rounded': isRounded}"
  >
    <slot name="button"/>
  </CompanyListButton>
  <DropDownMenu
      v-if="isActive"
      @closeDropDownMenu="this.isActive=false"
  >
    <slot name="menu"/>
  </DropDownMenu>
</template>

<script lang="ts">
import CompanyListButton from "@/components/company_list/CompanyListButton.vue";
import DropDownMenu from "@/components/UI/DropDownMenu.vue";

export default {
  name: 'DropDownMenuBox',
  components: {DropDownMenu, CompanyListButton},
  data() {
    return {
      isActive: false
    }
  },
  props: {
    isRounded: Boolean
  },
}
</script>

<style scoped>

</style>