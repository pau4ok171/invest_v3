<script lang="ts">
import {defineComponent} from 'vue'
import CircledButton from "@/components/UI/buttons/CircledButton.vue";
import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailModalMenu",
  components: {
    ModalMenuCloseIcon,
    CircledButton
  },
  computed: {
    ...mapGetters({
      notesModalIsLateral: "companyDetail/getNotesModalMenuIsLateral",
    }),
  },
})
</script>

<template>
<div class="detail_modal_menu__wrapper" v-if="!notesModalIsLateral"></div>

<div class="detail_modal_menu" :class="{'detail_modal_menu--lateral': notesModalIsLateral}">
  <slot/>
</div>

</template>

<style>
.detail_modal_menu__wrapper {
  z-index: 9999;
  position: fixed;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  background-color: #000;
  opacity: 0.8;
  transition: opacity .4s cubic-bezier(.23, 1, .32, 1) 0s;
}
.detail_modal_menu {
  z-index: 9999;
  position: fixed;
  display: grid;
  grid-template-rows: auto 1fr auto;
  width: 100%;
  height: calc(100dvh - 40px);
  max-width: 886px;
  overflow-x: hidden;
  top: auto;
  right: max(0px, 50vw - 443px);
  bottom: 0;
  background-color: #1b222d;
  border: 1px solid rgb(38, 46, 58);
  touch-action: none;
  color: #8c929b;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  box-shadow: rgba(11, 14, 19, .25) -10px -10px 10px, rgba(11, 14, 19, .1) 10px 10px 10px;
  transform: translate3d(0px, 0%, 0px);
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, top 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, right 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, max-width 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, height 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s;
}
.detail_modal_menu--lateral {
  left: auto;
  right: 40px;
  width: 433px;
  height: 420px;
  padding: 0;
  overflow: visible;
  transform: translate3d(0px, 0%, 0px);
}
.detail_modal_menu--lateral .detail_modal_menu__main {
    min-height: 200px;
    height: 270px;
}
</style>