<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default defineComponent({
  name: "RoundedBorderedButton",
  components: {RoundedButton}
})
</script>

<template>
  <RoundedButton class="button--bordered">
    <slot/>
  </RoundedButton>
</template>

<style scoped>
  .button--bordered {
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, .2);
  }
</style>