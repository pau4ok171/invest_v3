<template>
  <RoundedButton class="button--blue-dark">
    <slot/>
  </RoundedButton>
</template>

<script lang="ts">
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default {
  name: "RoundedBlueButton",
  components: {RoundedButton}
}
</script>

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