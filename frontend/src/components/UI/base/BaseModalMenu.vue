<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "BaseModalMenu",
  components: {
  },
})
</script>

<template>
<div class="base_modal_menu__wrapper">
  <div class="base_modal_menu">
    <slot/>
  </div>
</div>
</template>

<style scoped>
.base_modal_menu__wrapper {
  width: 100%;
  background-color: rgba(38, 46, 58, .4);
  padding: 32px;
  top: 0;
  left: 0;
  position: fixed;
  height: 100%;
  z-index: 9999;
  display: flex;
  flex-flow: wrap;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}
.base_modal_menu {
  width: 700px;
  max-height: 530px;
  background-color: #fff;
  color: #000;
}
</style>