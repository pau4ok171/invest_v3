<template>
  <div class="form__field">
    <fieldset class="form__fieldset">
      <slot/>
    </fieldset>
  </div>
</template>

<script lang="ts">
 export default {
   name: 'AuthField',
 }
</script>

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