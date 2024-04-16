<script lang="ts">
import {defineComponent} from 'vue'
import TextButton from "@/components/UI/buttons/TextButton.vue";

export default defineComponent({
  name: "TextBlueButton",
  components: {TextButton}
})
</script>

<template>
  <TextButton class="button--text-format-blue">
    <slot/>
  </TextButton>
</template>

<style>
  .button--text-format-blue {
    color: var(--blue);
    box-shadow: none;
  }
  .button--text-format-blue:not([disabled]):hover {
    background-color: transparent;
    box-shadow: var(--blue) 0 -1px 0 0 inset;
  }
  .button--text-format-blue span {
    color: var(--blue);
    font-size: 1.4rem;
    line-height: 1.5;
  }
  .button--text-format-blue svg {
    fill: var(--blue);
  }
</style>