<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default defineComponent({
  name: "RoundedDarkBlueButton",
  components: {RoundedButton},
  props: {
    isFullWidth: {
      type: Boolean,
      default: false,
    },
  }
})
</script>

<template>
  <RoundedButton :class="['button--high-dark', {'button--full-width': isFullWidth}]">
    <slot/>
  </RoundedButton>
</template>

<style>
  .button--high-dark {
    background-color: rgba(53, 110, 233, .1);
    color: var(--blue);
  }
  .button--high-dark svg {
    fill: var(--blue);
  }
  .button--high-dark span {
    color: var(--blue);
  }
  .button--high-dark:not([disabled]):hover {
    background-color: rgba(53, 110, 233, .2);
  }
  .button--full-width {
    width: 100%;
    justify-content: center;
  }

</style>