<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default defineComponent({
  name: "RoundedSuccessButton",
  components: {
    RoundedButton,
  }
})
</script>

<template>
<RoundedButton class="button--success">
  <slot/>
</RoundedButton>
</template>

<style>
.button--success {
  background-color: #2dc97e;
}
.button--success svg {
  fill: #fff;
}
.button--success span {
  color: #fff;
}
.button--success[disabled] {
  opacity: 1;
}
</style>