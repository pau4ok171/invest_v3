<script lang="ts">
import {defineComponent} from 'vue'
import BaseButton from "@/components/UI/buttons/BaseButton.vue";

export default defineComponent({
  name: "BaseInvisibleButton",
  components: {
    BaseButton,
  }
})
</script>

<template>
<BaseButton class="button--invisible">
  <slot/>
</BaseButton>
</template>

<style scoped>
.button--invisible {
  background-color: transparent;
  justify-content: center;
  height: 30px;
}
.button--invisible[disabled] {
  background-color: rgba(0, 0, 0, .3);
  opacity: 1;
  cursor: auto;
}
.button--invisible:not([disabled]):hover {
  color: var(--blue-hover);
}
</style>