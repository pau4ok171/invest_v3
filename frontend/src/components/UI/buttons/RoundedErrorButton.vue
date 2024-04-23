<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default defineComponent({
  name: "RoundedErrorButton",
  components: {RoundedButton}
})
</script>

<template>
<RoundedButton class="button--error">
  <slot/>
</RoundedButton>
</template>

<style>
.button--error {
  background-color: #e64141;
}
.button--error svg {
  fill: #fff;
}
.button--error span {
  color: #fff;
}
.button--error:not([disabled]):hover {
  background-color: #ac2121;
}
</style>