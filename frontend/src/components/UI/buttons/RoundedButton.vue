<template>
  <BaseButton class="button--rounded">
    <slot/>
  </BaseButton>
</template>

<script lang="ts">
import BaseButton from "@/components/UI/buttons/BaseButton.vue";
export default {
  name: 'RoundedButton',
  components: {BaseButton},
}
</script>

<style>
  .button--rounded {
    height: 32px;
    font-size: 1.2rem;
  }
</style>