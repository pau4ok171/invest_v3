<template>
  <BaseButton class="button--circled">
    <slot/>
  </BaseButton>
</template>

<script lang="ts">
import BaseButton from "@/components/UI/buttons/BaseButton.vue";

export default {
  name: "CircledButton",
  components: {BaseButton}
}
</script>

<style>
  .button--circled {
    border-radius: 100%;
  }
</style>