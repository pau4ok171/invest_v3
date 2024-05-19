<script lang="ts">
  import {defineComponent} from "vue";

  export default defineComponent({
    name: 'AuthButton',
  })
</script>

<template>
<button class="form__button" type="submit">
  <slot/>
</button>
</template>

<style scoped>
.form__button {
  position: relative;
  transition: background-color .2s ease 0s;
  color: rgba(255, 255, 255, .7);
  border-radius: 6px;
  user-select: none;
  margin-top: 2.4rem;
  font-size: 1.4rem;
  color: #fff;
  padding: 0;
  background-color: rgb(35, 148, 223);
  width: 100%;
  height: 40px;
}
.form__button:hover {
  background-color: rgb(32, 112, 165);
}
.form__button:disabled {
  opacity: .3;
  cursor: auto;
  pointer-events: none;
}
</style>