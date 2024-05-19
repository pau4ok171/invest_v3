<script lang="ts">
 import {defineComponent} from "vue";

 export default defineComponent({
   name: 'AuthField',
 })
</script>

<template>
<div class="form__field">
  <fieldset class="form__fieldset">
    <slot/>
  </fieldset>
</div>
</template>

<style>
.form__field {
  position: relative;
  margin-bottom: 2.4rem;
}
.form__fieldset {
  margin: 0;
  position: relative;
  padding-top: 24px;
  border: transparent;
}
</style>