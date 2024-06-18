<script lang="ts">
import {defineComponent} from 'vue'
import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";
import RoundedGreyButton from "@/components/UI/buttons/RoundedGreyButton.vue";

export default defineComponent({
  name: "BaseLateralMenu",
  components: {RoundedGreyButton, ModalMenuCloseIcon}
})
</script>

<template>
<div class="base-lateral-menu">
  <div class="base-lateral-menu__inner">
    <header class="base-lateral-menu__header">
      <h3 class="base-lateral-menu__title">
        <slot name="title"/>
      </h3>
      <RoundedGreyButton class="base-lateral-menu__close-button" @click="$emit('closeMenu')">
        <ModalMenuCloseIcon/>
      </RoundedGreyButton>
    </header>
    <main class="base-lateral-menu__main">
      <slot name="content"/>
    </main>
  </div>
</div>
</template>

<style>
.base-lateral-menu {
  position: fixed;
  left: 1368px;
  top: 76px;
  right: 4px;
  width: 377px;
  height: calc(-88px + 100vh);
  overflow: hidden;
  color: rgb(201, 203, 207);
}
.base-lateral-menu__inner {
  position: relative;
  height: 100%;
  background-color: rgb(27, 34, 45);
  padding: 16px;
  border-radius: 8px;
}
.base-lateral-menu__header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}
.base-lateral-menu__title {
  font-size: 2rem;
  font-weight: normal;
  color: rgb(255, 255, 255);
  line-height: 1.5;
}
.base-lateral-menu__close-button svg {
  width: 20px;
  height: 20px;
  fill: white;
  opacity: 0.5;
}
</style>