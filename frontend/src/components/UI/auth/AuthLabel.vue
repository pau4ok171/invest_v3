<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
 name: 'AuthLabel'
})
</script>

<template>
<label for="username" class="form__label">
  <slot/>
</label>
</template>

<style scoped>
.form__label {
  display: block;
  color: rgb(38, 46, 58);
  position: absolute;
  top: 0;
  left: 0;
  margin-bottom: 0;
  transition: opacity .3s ease 0s;
  line-height: 1.5;
}
</style>