<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: 'DropDownMenu',
  methods: {
    clickHandler(event: Event) {
      const target = event.target as HTMLDivElement
      if (target.parentNode !== this.$el.parentNode) {
        this.$emit('closeDropDownMenu')
        document.removeEventListener('click', this.clickHandler)
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.clickHandler)
  },
})
</script>

<template>
<div>
  <slot/>
</div>
</template>

<style>
.dropdown-menu::-webkit-scrollbar {
  width: 10px;
}
.dropdown-menu::-webkit-scrollbar-track {
  -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
  background-color: #f9f9fd;
  border-radius: 10px;
}
.dropdown-menu::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: linear-gradient(180deg, #00c6fb, #005bea);
}
</style>