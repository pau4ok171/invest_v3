<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: 'BaseButton',
})
</script>

<template>
<button
  @click="$emit('buttonClick')"
  class="button"
>
  <slot/>
</button>
</template>

<style>
.button {
  display: flex;
  align-items: center;
  height: 40px;
  padding: 0 12px;
  border-radius: 8px;
  font-size: 1.4rem;
  color: rgba(255, 255, 255, .7);
  background-color: transparent;
  transition: background-color .2s ease 0s;
  user-select: none;
}
.button:not([disabled]):hover {
  background-color: rgba(255, 255, 255, .05);
}
.button[disabled] {
  opacity: .5;
  cursor: auto;
}
.button span {
  color: #fff;
  pointer-events: none;
  margin: 0 4px;
}
.button svg {
  width: 24px;
  height: 24px;
  fill: rgba(255, 255, 255, .5);
  pointer-events: none;
  margin: 0 -4px;
}
</style>