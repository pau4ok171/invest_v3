<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import RoundedGreyButton from "@/components/UI/buttons/RoundedGreyButton.vue";

export default defineComponent({
  name: "RoundedHighGreyButton",
  components: {RoundedGreyButton, RoundedButton}
})
</script>

<template>
<RoundedGreyButton class="button--high button--bg_grey">
  <slot/>
</RoundedGreyButton>
</template>

<style>
.button--high {
  height: 40px;
}
.button--bg_grey {
  background-color: #e8e8e8;
}
.button--bg_grey:not([disabled]):hover {
  background-color: rgba(38, 46, 58, .15);
}
</style>