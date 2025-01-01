<script lang="ts">
import {defineComponent} from 'vue'
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "BaseModalMenu",
  components: {
    BaseButton,
  },
})
</script>

<template>
<div class="base_modal_menu__wrapper">
  <div class="base_modal_menu">

    <header class="base_modal_menu__header">
      <h1 class="base_modal_menu__title">
        <slot name="title"/>
      </h1>
      <base-button
        icon="ModalMenuCloseIcon"
        variant="text"
        color="#92969c"
        rounded="x-small"
        density="comfortable"
        theme="grey"
       @click="$emit('closeMenu')"
      />

    </header>

    <main class="base_modal_menu__main">
      <slot name="content"/>
    </main>

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
  z-index: 1000;
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
.base_modal_menu__header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #e8e8e8;
}
.base_modal_menu__title {
  font-size: 2rem;
  line-height: 1.5;
  font-weight: 500;
  color: #262e3a;
}
.base_modal_menu__main {
  max-height: 392px;
  overflow-y: auto;
  padding: 0;
  border-bottom: none;
}
.base_modal_menu__main::-webkit-scrollbar {
  width: 10px;
}
.base_modal_menu__main::-webkit-scrollbar-track {
	-webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
	background-color: #f9f9fd;
	border-radius: 10px;
}
.base_modal_menu__main::-webkit-scrollbar-thumb {
	border-radius: 10px;
	background: linear-gradient(180deg, #00c6fb, #005bea);
}
</style>