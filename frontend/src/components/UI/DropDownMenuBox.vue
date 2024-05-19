<script lang="ts">
import DropDownMenu from "@/components/UI/DropDownMenu.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'DropDownMenuBox',
  components: {
    DropDownMenu,
  },
  data() {
    return {
      isActive: false
    }
  },
})
</script>

<template>
<div class="drop-down-menu__button" @click="isActive=!isActive">

  <slot name="button"/>

  <DropDownMenu v-if="isActive" @closeDropDownMenu="isActive=false">
    <slot name="menu"/>
  </DropDownMenu>

</div>
</template>

<style>
.drop-down-menu__button{
  position: relative;
}
</style>