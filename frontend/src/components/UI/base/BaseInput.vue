<template>
  <input type="text" class="input" :value="inputValue"  @input="updateInput" placeholder="Type to input...">
</template>

<script lang="ts">
  export default {
    name: 'BaseInput',
    props: {
      inputValue: [Number, String],
    },
    methods: {
      updateInput(event) {
        this.$emit('updateInput', event.target.value)
      }
    },
  }
</script>

<style scoped>

</style>