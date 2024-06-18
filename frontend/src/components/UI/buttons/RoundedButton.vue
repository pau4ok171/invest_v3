<script lang="ts">
import BaseButton from "@/components/UI/buttons/BaseButton.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'RoundedButton',
  components: {
    BaseButton,
  },
})
</script>

<template>
<BaseButton class="button--rounded">
  <slot/>
</BaseButton>
</template>

<style>
.button--rounded {
  height: 32px;
  font-size: 1.2rem;
}
.is-active {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>