<template>
  <div @click="isActive=!isActive">
    <slot
      name="button"
    />
  <DropDownMenu
      v-if="isActive"
      @closeDropDownMenu="this.isActive=false"
  >
    <slot name="menu"/>
  </DropDownMenu>
  </div>
</template>

<script lang="ts">
import DropDownMenu from "@/components/UI/DropDownMenu.vue";

export default {
  name: 'DropDownMenuBox',
  components: {DropDownMenu},
  data() {
    return {
      isActive: false
    }
  },
}
</script>
