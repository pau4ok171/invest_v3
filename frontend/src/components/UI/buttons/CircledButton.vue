<script lang="ts">
import BaseButton from "@/components/UI/buttons/BaseButton.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: "CircledButton",
  components: {BaseButton}
})
</script>

<template>
<BaseButton class="button--circled">
  <slot/>
</BaseButton>
</template>

<style>
.button--circled {
  border-radius: 100%;
}
</style>