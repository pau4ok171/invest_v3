<template>
<div class="modal_menu__wrapper">
  <div class="modal_menu">
    <div class="login__login-form">
      <button class="modal_menu__header-close-button" @click="closeModalMenu"><ModalMenuCloseIcon/></button>
      <slot/>
    </div>
  </div>
</div>
</template>

<script  lang="ts">
  import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";

  export default {
    name: 'ModalMenu',
    components: {
      ModalMenuCloseIcon
    },
    data() {
      return {
      }
    },
    methods: {
      closeModalMenu() {
        this.$emit('closeModalMenu')
      }
    },
  }
</script>

<style scoped>
  .modal_menu__wrapper {
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
    transition: visibility 0s .6s, opacity .6s ease;
    overflow: hidden;
  }
  .modal_menu {
    position: relative;
    width: 456px;
    height: min-content;
    background-color: #fff;
    border-radius: 8px;
    color: #000;
  }
  .modal_menu__header-close-button {
    position: absolute;
    top: 0;
    right: 0;
    padding: 5px;
    z-index: 10;
    border-radius: 8px;
    transition: background-color .2s ease-out;
  }
  .modal_menu__header-close-button:hover {
      background-color: rgba(38, 46, 58, .05);
  }
  .modal_menu__header-close-button svg {
      width: 24px;
      height: 24px;
      vertical-align: middle;
      fill: #92969c;
      pointer-events: none;
  }
</style>