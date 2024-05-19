<script lang="ts">
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: "RoundedBlueButton",
  components: {RoundedButton}
})
</script>

<template>
<RoundedButton class="button--blue-dark">
  <slot/>
</RoundedButton>
</template>

<style>
.button--blue-dark {
  background-color: var(--blue);
  color: #fff;
}
.button--blue-dark svg {
  fill: #fff;
}
.button--blue-dark span {
  color: inherit;
}
.button--blue-dark:not([disabled]):hover {
  background-color: var(--blue-hover);
}
</style>