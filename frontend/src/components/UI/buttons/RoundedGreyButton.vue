<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default defineComponent({
  name: "RoundedGreyButton",
  components: {RoundedButton}
})
</script>

<template>
<RoundedButton class="button--grey">
 <slot/>
</RoundedButton>
</template>

<style>
.button--grey svg {
  fill: #92969c;
}
.button--grey span {
  color: #000;
}
.button--grey span {
  color: #000;
}
.button--grey:not([disabled]):hover {
  background-color: rgba(38, 46, 58, .05);
}
</style>