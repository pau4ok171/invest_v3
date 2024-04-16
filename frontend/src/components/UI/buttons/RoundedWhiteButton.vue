<template>
  <RoundedButton class="button--white-light">
    <slot/>
  </RoundedButton>
</template>

<script lang="ts">
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default {
  name: "RoundedWhiteButton",
  components: {RoundedButton}
}
</script>

<style>
  .button--white-light {
    background-color: #fff;
    color: #000;
  }
  .button--white-light svg {
    fill: #000;
  }
  .button--white-light span {
    color: inherit;
  }
  .button--white-light:not([disabled]):hover {
    background-color: var(--white-hover);
  }
</style>