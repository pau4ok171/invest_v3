<template>
  <BaseButton class="button--text-format">
    <slot/>
  </BaseButton>
</template>

<script lang="ts">
import BaseButton from "@/components/UI/buttons/BaseButton.vue";
export default {
  name: 'TextButton',
  components: {BaseButton},
}
</script>

<style>
  .button--text-format {
    color: inherit;
    position: relative;
    height: auto;
    transition: all .3s ease 0s;
    vertical-align: middle;
    font-size: 1.2rem;
    font-weight: normal;
    background-color: transparent;
    border-radius: 0;
    padding: 0;
    border: 0;
    box-shadow: rgba(255, 255, 255, .5) 0 -1px 0 0 inset;
  }
  .button--text-format:not([disabled]):hover {
    background-color: inherit;
    box-shadow: rgba(255, 255, 255, .8) 0 -1px 0 0 inset;
  }
</style>